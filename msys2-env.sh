# Sourced by the Windows build/run scripts: puts the MSYS2 CLANG64 toolchain first on PATH.
# MSYS2_ROOT overrides the default C:/msys64.
msys2_root=${MSYS2_ROOT:-/c/msys64}
if [[ ! -d $msys2_root/clang64/bin ]]; then
    # MSYS2 somewhere else: this shell lives in <root>/usr/bin, so climb out of it. The result
    # may be / itself when the script runs inside that install, which needs no leading prefix.
    msys2_root=$(cd -- "$(dirname -- "$(command -v bash)")/../.." && pwd)
fi
msys2_root=${msys2_root%/}
clang64_bin=$msys2_root/clang64/bin
# The compiler is named clang on newer CLANG64 packages and clangcc on some older ones.
[[ -n ${CC:-} ]] || for compiler in clang clangcc; do
    [[ -x $clang64_bin/$compiler.exe ]] && { CC=$compiler; break; }
done
if [[ -d $clang64_bin ]]; then
    export PATH="$clang64_bin:$msys2_root/usr/bin:$PATH"
    export MSYSTEM=CLANG64
    export CC
fi
