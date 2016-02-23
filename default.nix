with import <nixpkgs> {}; {
  dadaportalEnv = stdenv.mkDerivation {
    name = "dadaportal";
    buildInputs = [
      python35
      python35Packages.pillow
      python35Packages.lxml
    ];
  };
}
