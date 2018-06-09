%% Generate Data Vector Figures

%% 20 dB SNR
figure;
gen_subplot('../data/bpsk20.dat', 'BPSK',    3,4,1);
gen_subplot('../data/qpsk20.dat', 'QPSK',    3,4,2);
gen_subplot('../data/8psk20.dat', '8PSK',    3,4,3);
gen_subplot('../data/pam420.dat', 'PAM4',    3,4,4);
gen_subplot('../data/qam1620.dat', 'QAM16',  3,4,5);
gen_subplot('../data/qam6420.dat', 'QAM64',  3,4,6);
gen_subplot('../data/gfsk20.dat', 'GFSK',    3,4,7);
gen_subplot('../data/cpfsk20.dat', 'CPFSK',  3,4,8);
gen_subplot('../data/amssb20.dat', 'AM-SSB', 3,4,9);
gen_subplot('../data/amdsb20.dat', 'AM-DSB', 3,4,10);
gen_subplot('../data/wbfm20.dat', 'WBFM',    3,4,11);


%% 0 dB SNR
figure;
gen_subplot('../data/bpsk0.dat', 'BPSK',    3,4,1);
gen_subplot('../data/qpsk0.dat', 'QPSK',    3,4,2);
gen_subplot('../data/8psk0.dat', '8PSK',    3,4,3);
gen_subplot('../data/pam40.dat', 'PAM4',    3,4,4);
gen_subplot('../data/qam160.dat', 'QAM16',  3,4,5);
gen_subplot('../data/qam640.dat', 'QAM64',  3,4,6);
gen_subplot('../data/gfsk0.dat', 'GFSK',    3,4,7);
gen_subplot('../data/cpfsk0.dat', 'CPFSK',  3,4,8);
gen_subplot('../data/amssb0.dat', 'AM-SSB', 3,4,9);
gen_subplot('../data/amdsb0.dat', 'AM-DSB', 3,4,10);
gen_subplot('../data/wbfm0.dat', 'WBFM',    3,4,11);

%% -20 dB SNR
figure;
gen_subplot('../data/bpsk-20.dat', 'BPSK',   3,4,1);
gen_subplot('../data/qpsk-20.dat', 'QPSK',   3,4,2);
gen_subplot('../data/8psk-20.dat', '8PSK',   3,4,3);
gen_subplot('../data/pam4-20.dat', 'PAM4',   3,4,4);
gen_subplot('../data/qam16-20.dat', 'QAM16', 3,4,5);
gen_subplot('../data/qam64-20.dat', 'QAM64', 3,4,6);
gen_subplot('../data/gfsk-20.dat', 'GFSK',   3,4,7);
gen_subplot('../data/cpfsk-20.dat', 'CPFSK', 3,4,8);
gen_subplot('../data/amssb-20.dat', 'AM-SSB',3,4,9);
gen_subplot('../data/amdsb-20.dat', 'AM-DSB',3,4,10);
gen_subplot('../data/wbfm-20.dat', 'WBFM',   3,4,11);

