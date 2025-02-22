{
  description = "Automatic translator for light novels";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";

    nixcode = {
      url = "github:Dessera/nixcode";
      inputs.flake-parts.follows = "flake-parts";
    };

    pyproject-nix = {
      url = "github:pyproject-nix/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    uv2nix = {
      url = "github:pyproject-nix/uv2nix";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    pyproject-build-systems = {
      url = "github:pyproject-nix/build-system-pkgs";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.uv2nix.follows = "uv2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  nixConfig = {
    extra-substituters = [
      "https://nixcode.cachix.org"
    ];

    extra-trusted-public-keys = [
      "nixcode.cachix.org-1:6FvhF+vlN7gCzQ10JIKVldbG59VfYVzxhH/+KGHvMhw="
    ];
  };

  outputs =
    {
      nixpkgs,
      flake-parts,
      pyproject-nix,
      uv2nix,
      pyproject-build-systems,
      ...
    }@inputs:
    flake-parts.lib.mkFlake { inherit inputs; } (
      { withSystem, ... }:
      {
        systems = [ "x86_64-linux" ];

        perSystem =
          { system, ... }:
          let
            pkgs = import nixpkgs {
              inherit system;
              config = {
                allowUnfree = true;
              };
            };

            
            python = pkgs.python313;
            code = withSystem system ({ inputs', ... }: inputs'.nixcode.packages.nixcode-python);

            py = import ./python.nix {
              inherit
                pkgs
                python
                uv2nix
                pyproject-nix
                pyproject-build-systems
                ;
            };
          in
          {
            packages = {
              default = py.packages.default;
            };

            devShells = {
              default = pkgs.mkShell {
                packages =
                  [
                    py.env.editable
                    code
                  ]
                  ++ (with pkgs; [
                    uv
                    nixd
                    nixfmt-rfc-style
                  ]);
                env = {
                  UV_NO_SYNC = "1";
                  UV_PYTHON_DOWNLOADS = "never";
                  UV_PYTHON = "${py.env.editable}/bin/python";
                };
                shellHook = ''
                  unset PYTHONPATH
                  export REPO_ROOT=$(git rev-parse --show-toplevel)
                '';
              };

              uv = pkgs.mkShell {
                packages = [ python pkgs.uv ];

                env = {
                  UV_NO_SYNC = "1";
                  UV_PYTHON_DOWNLOADS = "never";
                  UV_PYTHON = "${python}/bin/python";
                };
                shellHook = ''
                  unset PYTHONPATH
                  export REPO_ROOT=$(git rev-parse --show-toplevel)
                '';
              };
            };
          };
      }
    );
}
