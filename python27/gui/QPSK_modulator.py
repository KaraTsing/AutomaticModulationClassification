# simple QT QPSK modulator class

class QPSK_modulator:
    def __init__(top_layout):
        self.top_layout = top_layout
        
    def start():
        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1e6

        ##################################################
        # Blocks
        ##################################################
        
        ##################################
        # USRP block
        ##################################
        # self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	# ",".join(("", "")),
        	# uhd.stream_args(
        		# cpu_format="fc32",
        		# channels=range(1),
        	# ),
        # )
        # self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        # self.uhd_usrp_sink_0.set_center_freq(1e9, 0)
        # self.uhd_usrp_sink_0.set_gain(15, 0)
        
        ##################################
        # Freq sink block
        ##################################
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	512, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(0.1)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)

        if not True:
          self.qtgui_freq_sink_x_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        
        
        ##################################
        # Noise model block
        ##################################
        self.channels_channel_model_0 = channels.channel_model(
        	noise_voltage=10**(-20/10),
        	frequency_offset=0.0,
        	epsilon=1.0, # 1 means no difference
        	taps=(1.0 + 1.0j, ), # taps=(0,), 
        	noise_seed=0,
        	block_tags=False
        )
        
       
        ##################################
        # modulator block
        ##################################
        src, mod, chan = gen_amssb(self.channel_prop)
        
        rsrc = self.create_rand_block('digital')
        asrc = self.create_rand_block('analog')
        
        ##################################################
        # Connections
        ##################################################
        # self.connect((src, 0), (mod, 0), (self.channels_channel_model_0, 0))
        # self.connect((self.channels_channel_model_0, 0),  (self.qtgui_freq_sink_x_0, 0))
        # self.connect((self.channels_channel_model_0, 0), (self.uhd_usrp_sink_0, 0))
        
        self.connect((src, 0), (mod, 0))
        self.connect((mod, 0),  (self.qtgui_freq_sink_x_0, 0))
        #self.connect((mod, 0), (self.uhd_usrp_sink_0, 0))
        
    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.channels_cfo_model_1.set_samp_rate(self.samp_rate)
        self.channels_cfo_model_0.set_samp_rate(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.analog_sig_source_x_1.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        
    def handle_QPSK(self):
        # generate data 
        self.statusLabel.setText("Status: Generating QPSK Data" + " SNR: " + str(self.SNRSlider.value()))
        src, mod, chan = gen_qpsk(self.channel_prop)
        noise_gen = self.generate_noise()
        
        # set up new display using the given model
        self.lock()
        self.disconnect_all()
        self.connect((src, 0), (mod, 0), (noise_gen, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect(noise_gen, self.uhd_usrp_sink_0)
        self.unlock()
        
        
    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()