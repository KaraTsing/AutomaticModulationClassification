%% GnuRadio Data Reader



%% 8PSK
gen_comparison('fromjetson/8psk_20_auto.dat', 'fromjetson/sample1/vec_8PSK-18.vec')

%% AM-DSB
gen_comparison('fromjetson/amdsb_20_auto.dat', 'fromjetson/sample1/vec_AM-DSB-18.vec')

%% BPSK
gen_comparison('fromjetson/bpsk_20_auto.dat', 'fromjetson/sample1/vec_BPSK-18.vec')

%% CPFSK
gen_comparison('fromjetson/cpfsk_20_auto.dat', 'fromjetson/sample1/vec_CPFSK-18.vec')

%% GFSK

%% PAM4
gen_comparison('fromjetson/pam4_20_auto.dat', 'fromjetson/sample1/vec_PAM4-18.vec')

%% QAM16
gen_comparison('fromjetson/qam16_20_auto.dat', 'fromjetson/sample1/vec_QAM16-18.vec')

%% QAM64
gen_comparison('fromjetson/qam64_20_auto.dat', 'fromjetson/sample1/vec_QAM64-18.vec')

%% WBFM
%gen_comparison('fromjetson/wbfm_20_auto.dat', 'fromjetson/sample1/vec_WBFM-18.vec')

%% AMSSB
gen_comparison('fromjetson/amssb_20_auto.dat', 'fromjetson/sample1/vec_AM-SSB-18.vec')

%% 8psk_tr
gen_comparison('fromjetson/8pfsk_20_auto_tc_2.dat', 'fromjetson/sample1/vec_8PSK-18.vec')

%%
break;


bpsk = read_complex_binary('bpsk_20.dat', 1024);

cpfsk = read_complex_binary('cpfsk_20.dat', 1024);

plot(1:1024, real(bpsk), 1:1024, imag(bpsk));
figure;
plot(1:1024, real(cpfsk), 1:1024, imag(cpfsk));

%% plot comparison
len = 128;
bpsk = read_complex_binary('fromjetson/bpsk_20_auto.dat', len);
bpsk_check = read_rf_vec('fromjetson/bpsk_20_auto_tr.dat', len);
if (bpsk ~= transpose(bpsk_check))
    disp('problem reading file')
end

bpsk_tr = read_rf_vec('fromjetson/sample1/vec_BPSK-18.vec', len);


figure; 
subplot(2,1,1);
plot(1:len, real(bpsk_check), 1:len, imag(bpsk_check));
subplot(2,1,2);
plot(1:len, real(bpsk_tr), 1:len, imag(bpsk_tr));

%% plot comparison
len = 128;
psk8 = read_complex_binary('fromjetson/8psk_20_auto.dat', len);
psk8_check = read_rf_vec('fromjetson/8psk_20_auto_tr.dat', len);
if (psk8 ~= transpose(psk8_check))
    disp('problem reading file')
end

psk8_tr = read_rf_vec('fromjetson/sample1/vec_8PSK-18.vec', len);


figure; 
subplot(2,1,1);
plot(1:len, real(psk8_check), 1:len, imag(psk8_check));
subplot(2,1,2);
plot(1:len, real(psk8_tr), 1:len, imag(psk8_tr));

hold on;
plot(abs(fftshift(fft(psk8_check))))
plot(abs(fftshift(fft(psk8_tr))))
hold off;
%% plot comparison
len = 128;
cpfsk = read_complex_binary('fromjetson/cpfsk_20_auto.dat', len);
cpfsk_check = read_rf_vec('fromjetson/cpfsk_20_auto_tr.dat', len);
if (cpfsk ~= transpose(cpfsk_check))
    disp('problem reading file')
end

cpfsk_tr = read_rf_vec('fromjetson/sample1/vec_CPFSK-18.vec', len);


figure; 
subplot(2,1,1);
plot(1:len, real(cpfsk_check), 1:len, imag(cpfsk_check));
subplot(2,1,2);
plot(1:len, real(cpfsk_tr), 1:len, imag(cpfsk_tr));

%% plot comparison
len = 128;
amdsb = read_complex_binary('fromjetson/amdsb_20_auto.dat', len);
amdsbc = read_rf_vec('fromjetson/amdsb_20_auto_tr.dat', len);
if (amdsb ~= transpose(amdsbc))
    disp('problem reading file')
end

amdsb_tr = read_rf_vec('fromjetson/sample1/vec_AM-DSB-18.vec', len);


figure; 
subplot(2,1,1);
plot(1:len, real(amdsbc), 1:len, imag(amdsbc));
subplot(2,1,2);
plot(1:len, real(amdsb_tr), 1:len, imag(amdsb_tr));


figure; plot(abs(fftshift(fft(amdsbc(60:end)))))
figure; plot(abs(fftshift(fft(amdsb_tr))))

