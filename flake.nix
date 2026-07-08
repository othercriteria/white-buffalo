{
  description = "White Buffalo - writing and illustration environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs {
        inherit system;
        config.allowUnfree = true;
        config.cudaSupport = true;
      };
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        packages = with pkgs; [
          # Writing / build
          git
          git-lfs
          gnumake
          pandoc
          vale

          # Image generation (Python env managed by uv; see imagegen/)
          uv
          ruff

          # Native-extension and CUDA support for torch/diffusers
          stdenv.cc.cc.lib
          zlib
          cudaPackages.cudatoolkit
          cudaPackages.cudnn

          # OpenCV runtime deps
          libGL
          libGLU
          xorg.libX11
          xorg.libXext
          glib
        ];

        LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
          pkgs.stdenv.cc.cc.lib
          pkgs.zlib
          pkgs.cudaPackages.cudatoolkit
          pkgs.cudaPackages.cudnn
          pkgs.libGL
          pkgs.libGLU
          pkgs.glib
          "/run/opengl-driver"
        ];

        shellHook = ''
          export HF_TOKEN=$(cat /etc/nixos/secrets/huggingface-token-2025-12-14 2>/dev/null || echo "")
          echo "White Buffalo environment ready."
          echo "GPU: $(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null || echo 'not detected')"
          [ -n "$HF_TOKEN" ] && echo "HF_TOKEN: configured" || echo "HF_TOKEN: not found"
        '';
      };
    };
}
