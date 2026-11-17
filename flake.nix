{
  description = "Vericoding: a Python concurrency workshop with TLA+";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" "aarch64-darwin" ];
      forAllSystems = f: nixpkgs.lib.genAttrs systems
        (system: f nixpkgs.legacyPackages.${system});
      tlaJar = pkgs: "${pkgs.tlaplus}/share/java/tla2tools.jar";
    in
    {
      devShells = forAllSystems (pkgs: {
        default = pkgs.mkShell {
          packages = [ pkgs.python312 pkgs.jdk21 ];
          TLA_JAR = tlaJar pkgs;
        };
      });

      checks = forAllSystems (pkgs: {
        default = pkgs.runCommand "tla-workshop-check" {
          nativeBuildInputs = [ pkgs.python312 ];
        } ''
          cp -r ${self} work
          chmod -R u+w work
          cd work
          python3 -m unittest discover -s code -v
          touch $out
        '';
      });

      formatter = forAllSystems (pkgs: pkgs.nixfmt-rfc-style);
    };
}
