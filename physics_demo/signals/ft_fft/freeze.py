from py2exe import freeze

includes = ["pandas","matplotlib.pyplot","numpy","time","pyqtgraph","PyQt5","PyQt5.QtWidgets","PyQt5.uic","sys","numpy","signal_processing.signal_processing"]
freeze(
    console=[{'script': 'Demo_signals_fft.py'}],
    windows=[],
    data_files=None,
    #zipfile='library.zip',
    #options={"includes": includes},
    version_info={}    
)
