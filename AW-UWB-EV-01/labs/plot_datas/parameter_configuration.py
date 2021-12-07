
import numpy as np

def main(pps,iter,fps):
    #*******parameters*********
    pulses_per_step = pps
    iterations = iter
    frame_rate = fps

    dac_min = 949
    dac_max = 1100

    #Chip register trx_dac_step_clog2
    dac_step = 1

    #Chip register trx_clocks_per_pulse
    prf_div = 16 

    #Chip register trx_dac_step_clog2
    dac_settle = 1

    rx_mframes = 128

    trx_backend_clk_prescale = 1

    #*******result**********
    backend_processing_clocks = rx_mframes * 3 + 1

    #(MHz)
    trx_backend_clk_frequency = 243 / 4 / trx_backend_clk_prescale

    #(us)
    backend_processing_time = backend_processing_clocks / trx_backend_clk_frequency

    #(MHz)
    PRF = 243 / prf_div

    clocks_per_step = pulses_per_step * prf_div + dac_settle

    steps_per_iteration = np.floor((dac_max - dac_min) / dac_step) + 1

    clocks_per_iteration = clocks_per_step * steps_per_iteration * iterations

    #(ms)
    frame_interval = 1000 / frame_rate
    #(ms)
    total_frame_time = (backend_processing_time + clocks_per_iteration / 243) / 1000
    #(Hz)
    max_fps = 1000 / total_frame_time
    #(%)
    duty_cycle = 100 * total_frame_time * 0.001 / (1 / frame_rate)
    #(ms)
    idle_time = frame_interval - total_frame_time

    print("******************************")
    print("pps:{},iter:{},fps:{}".format(pulses_per_step,iterations,frame_rate))

    print("******************************")
    print("total frame time:{:.2f}(ms)".format(total_frame_time))
    print("max fps:{:.2f}(Hz)".format(max_fps))
    print("duty cycle:{:.2f}(%)".format(duty_cycle))

    print("******************************")
    if iterations & (iterations - 1) != 0:
        print("iterations must be 2**n,otherwise,radar initialization will fail.")
    if frame_rate > 200:
        print("frame rate is too hight,the spi rates is not support yet and datas will be lost.")
    if duty_cycle > 100:
        print("duty cycle is too hight")


    



if __name__ == '__main__':
    pps = 128
    iter = 16
    fps = 49

    main(pps,iter,fps)

