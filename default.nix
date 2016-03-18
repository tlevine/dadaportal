with import <nixpkgs> {}; {
  scott2 = stdenv.mkDerivation {
    name = "scott2";
    buildInputs = with pkgs; [
      python35Packages.virtualenv
      python35Packages.pillow
      python35Packages.lxml
    ];
    shellHook =
    ''
      if test $(basename "$PWD") != dadaportal; then
        echo Run this from the dadaportal directory. > /dev/stderr
        exit 1
      fi
      test -d .virtualenv || virtualenv-3.5 .virtualenv
      . .virtualenv/bin/activate
      pip install -r requirements.txt
    '';
  };
}
