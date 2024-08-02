# https://docs.platformio.org/en/latest/scripting/examples/override_package_files.html

from os.path import join, isfile

Import("env","projenv")

libraries = { lib.name: lib for lib in  projenv.ConfigureProjectLibBuilder().depbuilders }


LMIC_DIR = libraries["IBM LMIC framework"].path
patchflag_path = join(LMIC_DIR, ".patching-done")

# patch file only if we didn't do it before
if not isfile(patchflag_path):
    original_file = join(LMIC_DIR, "src", "lmic", "config.h")
    patched_file = join("patches", "01_lmic_config.patch")

    assert isfile(original_file) and isfile(patched_file)

    env.Execute("patch '%s' '%s'" % (original_file, patched_file))
    
    def _touch(path):
        with open(path, "w") as fp:
            fp.write("")

    env.Execute(lambda *args, **kwargs: _touch(patchflag_path))