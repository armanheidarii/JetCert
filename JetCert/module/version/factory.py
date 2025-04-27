from module.version.base import CompilationModeTypes
from module.version.base.fast import FastCompilationToolTypes
from module.version.base.safe import SafeCompilationToolTypes
from module.version.base.fast.numba import NumbaVersion
from module.version.base.fast.codon import CodonVersion
from module.version.base.fast.python import PythonVersion
from module.version.base.safe.compcert import CompCertVersion


class Factory:
    repository = {
        CompilationModeTypes.FAST: {
            FastCompilationToolTypes.NUMBA: NumbaVersion,
            FastCompilationToolTypes.CODON: CodonVersion,
            FastCompilationToolTypes.PYTHON: PythonVersion,
        },
        CompilationModeTypes.SAFE: {SafeCompilationToolTypes.COMPCERT: CompCertVersion},
    }

    @classmethod
    def produce(cls, compilation_mode, compilation_tool):
        return cls.repository.get(compilation_mode).get(compilation_tool)
