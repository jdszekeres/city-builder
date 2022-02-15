{ pkgs }: {
    deps = [
        pkgs.bashInteractive
        pkgs.python39Full
        pkgs.poetry
        pkgs.python39Packages.flask
    ];
}