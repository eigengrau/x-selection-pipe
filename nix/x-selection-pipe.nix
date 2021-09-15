{ pkgs }:
pkgs.python38Packages.buildPythonApplication {
  pname = "x-selection-pipe";
  version = "0.1.0.0";
  nativeBuildInputs = [ pkgs.wrapGAppsHook ];
  propagatedBuildInputs = with pkgs; [
    python38Packages.pygobject3
    gtk3
    gobject-introspection
  ];
  src = ../.;
}
