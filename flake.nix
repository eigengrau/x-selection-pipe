{
  description = "x-selection-pipe";
  inputs = {
    nixpkgs.url = "nixpkgs/nixos-21.05";
    utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, utils }:
    (utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [
            (final: prev: {
              x-selection-pipe =
                final.callPackage ./nix/x-selection-pipe.nix { };
            })
          ];
        };
      in rec {
        packages.x-selection-pipe = pkgs.x-selection-pipe;
        defaultPackage = packages.x-selection-pipe;
        defaultApp = {
          type = "app";
          program = "${packages.x-selection-pipe}/bin/xselection-pipe";
        };
      }));
}
