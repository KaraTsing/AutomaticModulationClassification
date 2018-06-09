function gen_comparison(file_train, file_chan)

len = 128;
chan_vec = read_complex_binary(file_train, len);
train_vec = read_rf_vec(file_chan, len);



figure; 


subplot(2,2,1);
plot(1:len, real(chan_vec), 1:len, imag(chan_vec)); xlabel(file_train, 'Interpreter', 'none')
subplot(2,2,2);
plot(1:len, real(train_vec), 1:len, imag(train_vec)); xlabel(file_chan, 'Interpreter', 'none')

subplot(2,2,3);
plot(abs(fftshift(fft(chan_vec))))
subplot(2,2,4);
plot(abs(fftshift(fft(train_vec))))


end