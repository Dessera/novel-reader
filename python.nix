{
  pkgs,
  python,
  uv2nix,
  pyproject-nix,
  pyproject-build-systems,
}:
let
  util = pkgs.callPackage pyproject-nix.build.util {};

  workspace = uv2nix.lib.workspace.loadWorkspace {
    workspaceRoot = ./.;
  };

  overlay = workspace.mkPyprojectOverlay {
    sourcePreference = "wheel";
  };

  pyprojectOverrides = _final: _prev: {
  };

  pythonSet =
    (pkgs.callPackage pyproject-nix.build.packages {
      inherit python;
    }).overrideScope
      (
        pkgs.lib.composeManyExtensions [
          pyproject-build-systems.overlays.default
          overlay
          pyprojectOverrides
        ]
      );

  editableOverlay = workspace.mkEditablePyprojectOverlay {
    root = "$REPO_ROOT";
  };

  editablePythonSet = pythonSet.overrideScope (
    pkgs.lib.composeManyExtensions [
      editableOverlay
      (final: prev: {
        novel-reader = prev.novel-reader.overrideAttrs (old: {
          src = pkgs.lib.fileset.toSource {
            root = old.src;
            fileset = pkgs.lib.fileset.unions [
              (old.src + "/pyproject.toml")
              (old.src + "/README.md")
              (old.src + "/src/novel_reader/__init__.py")
            ];
          };
          nativeBuildInputs =
            old.nativeBuildInputs
            ++ (final.resolveBuildSystem {
              editables = [ ];
            });
        });
      })
    ]
  );
in
rec {
  packages = {
    default = util.mkApplication {
      venv = env.default;
      package = pythonSet.novel-reader;
    };
  };

  env = {
    default = pythonSet.mkVirtualEnv "novel-reader-env" workspace.deps.all;
    editable = editablePythonSet.mkVirtualEnv "novel-reader-dev-env" workspace.deps.all;
  };
}
