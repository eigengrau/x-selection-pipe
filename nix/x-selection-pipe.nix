{ gobject-introspection, gtk3, python3Packages, wrapGAppsHook }:
python3Packages.buildPythonApplication {
  pname = "x-selection-pipe";
  version = "0.1.0.0";
  nativeBuildInputs = [ wrapGAppsHook ];
  propagatedBuildInputs =
    [ python3Packages.pygobject3 gtk3 gobject-introspection ];
  src = ../.;
}
