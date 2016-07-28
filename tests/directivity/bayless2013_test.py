import time as time

import numpy as np

import openquake.hazardlib.geo as geo

from shakemap.grind.source import Source
import shakemap.grind.fault as fault
from shakemap.directivity.bayless2013 import Bayless2013
from shakemap.utils.timeutils import ShakeDateTime


def test_ss3():
    magnitude = 7.2
    dip = np.array([90])
    rake = 180.0
    width = np.array([15])
    fltx = np.array([0, 0])
    flty = np.array([0, 80])
    zp = np.array([0])
    epix = np.array([0])
    epiy = np.array([0.2 * flty[1]])

    # Convert to lat/lon
    proj = geo.utils.get_orthographic_projection(-122, -120, 39, 37)
    tlon, tlat = proj(fltx, flty, reverse=True)
    epilon, epilat = proj(epix, epiy, reverse=True)

    flt = fault.Fault.fromTrace(np.array([tlon[0]]), np.array([tlat[0]]),
                                np.array([tlon[1]]), np.array([tlat[1]]),
                                zp, width, dip, reference='ss3')

    event = {'lat': epilat[0],
             'lon': epilon[0],
             'depth': 10,
             'mag': magnitude,
             'id': 'ss3',
             'locstring': 'test',
             'type': 'SS',
             'timezone': 'UTC'}
    event['time'] = ShakeDateTime.utcfromtimestamp(int(time.time()))
    event['created'] = ShakeDateTime.utcfromtimestamp(int(time.time()))

    x = np.linspace(-60, 60, 21)
    y = np.linspace(-60, 138, 34)
    site_x, site_y = np.meshgrid(x, y)
    slon, slat = proj(site_x, site_y, reverse=True)
    deps = np.zeros_like(slon)
    source = Source(event, flt)
    source.setEventParam('rake', rake)

    test1 = Bayless2013(source, slat, slon, deps, T=1.0)

    # Test fd
    fd = test1.getFd()
    fd_test = np.array(
        [[0.00000000e+00, 0.00000000e+00, 2.14620746e-03,
          6.47899336e-03, 1.23119791e-02, 1.91676140e-02,
          2.64009788e-02, 3.32427846e-02, 3.88863288e-02,
          4.26104002e-02, 4.39120296e-02, 4.26104002e-02,
          3.88863288e-02, 3.32427846e-02, 2.64009788e-02,
          1.91676140e-02, 1.23119791e-02, 6.47899336e-03,
          2.14620746e-03, 0.00000000e+00, 0.00000000e+00],
         [0.00000000e+00, 8.57780996e-04, 3.99405791e-03,
          9.31948105e-03, 1.65406113e-02, 2.51316805e-02,
          3.43205435e-02, 4.31274592e-02, 5.04747209e-02,
          5.53634169e-02, 5.70796092e-02, 5.53634169e-02,
          5.04747209e-02, 4.31274592e-02, 3.43205435e-02,
          2.51316805e-02, 1.65406113e-02, 9.31948105e-03,
          3.99405791e-03, 8.57780996e-04, 0.00000000e+00],
            [-7.32594549e-04, 1.80425497e-04, 3.76908220e-03,
             1.00175179e-02, 1.86854835e-02, 2.92291145e-02,
             4.07487277e-02, 5.20057177e-02, 6.15509770e-02,
             6.79776087e-02, 7.02477931e-02, 6.79776087e-02,
             6.15509770e-02, 5.20057177e-02, 4.07487277e-02,
             2.92291145e-02, 1.86854835e-02, 1.00175179e-02,
             3.76908220e-03, 1.80425497e-04, -7.32594549e-04],
            [-3.29238561e-03, -2.60643191e-03, 1.16635260e-03,
             8.15185259e-03, 1.82290773e-02, 3.08983182e-02,
             4.51608038e-02, 5.94769126e-02, 7.18919113e-02,
             8.03888307e-02, 8.34165399e-02, 8.03888307e-02,
             7.18919113e-02, 5.94769126e-02, 4.51608038e-02,
             3.08983182e-02, 1.82290773e-02, 8.15185259e-03,
             1.16635260e-03, -2.60643191e-03, -3.29238561e-03],
            [-7.68543266e-03, -7.63179286e-03, -4.08866637e-03,
             3.27605236e-03, 1.45558215e-02, 2.94068040e-02,
             4.68176355e-02, 6.49397159e-02, 7.72066272e-02,
             8.50445368e-02, 8.77974692e-02, 8.50445368e-02,
             7.72066272e-02, 6.49397159e-02, 4.68176355e-02,
             2.94068040e-02, 1.45558215e-02, 3.27605236e-03,
             -4.08866637e-03, -7.63179286e-03, -7.68543266e-03],
            [-1.38078234e-02, -1.49011067e-02, -1.21731364e-02,
             -5.02168047e-03, 6.98177526e-03, 2.38268531e-02,
             4.30419205e-02, 6.00041964e-02, 7.44541603e-02,
             8.42939552e-02, 8.77989590e-02, 8.42939552e-02,
             7.44541603e-02, 6.00041964e-02, 4.30419205e-02,
             2.38268531e-02, 6.98177526e-03, -5.02168047e-03,
             -1.21731364e-02, -1.49011067e-02, -1.38078234e-02],
            [-2.13780396e-02, -2.42165379e-02, -2.30613142e-02,
             -1.70011475e-02, -5.15036128e-03, 1.25885635e-02,
             3.24536739e-02, 5.25619351e-02, 7.05100243e-02,
             8.31900906e-02, 8.78003567e-02, 8.31900906e-02,
             7.05100243e-02, 5.25619351e-02, 3.24536739e-02,
             1.25885635e-02, -5.15036128e-03, -1.70011475e-02,
             -2.30613142e-02, -2.42165379e-02, -2.13780396e-02],
            [-2.98882710e-02, -3.50862342e-02, -3.63793490e-02,
             -3.25716319e-02, -2.22546618e-02, -3.59274163e-03,
             1.83064517e-02, 4.20112440e-02, 6.46115966e-02,
             8.14746164e-02, 8.78016623e-02, 8.14746164e-02,
             6.46115966e-02, 4.20112440e-02, 1.83064517e-02,
             -3.59274163e-03, -2.22546618e-02, -3.25716319e-02,
             -3.63793490e-02, -3.50862342e-02, -2.98882710e-02],
            [-3.85810679e-02, -4.66488633e-02, -5.12430987e-02,
             -5.10089462e-02, -4.20856023e-02, -2.36905234e-02,
             -6.33876287e-04, 2.66765430e-02, 5.53289928e-02,
             7.86066125e-02, 8.78028757e-02, 7.86066125e-02,
             5.53289928e-02, 2.66765430e-02, -6.33876287e-04,
             -2.36905234e-02, -4.20856023e-02, -5.10089462e-02,
             -5.12430987e-02, -4.66488633e-02, -3.85810679e-02],
            [-4.64803335e-02, -5.76615888e-02, -6.61458422e-02,
             -7.06512643e-02, -6.38427394e-02, -4.77258398e-02,
             -2.55483969e-02, 4.05840724e-03, 3.98470070e-02,
             7.33053399e-02, 8.78039969e-02, 7.33053399e-02,
             3.98470070e-02, 4.05840724e-03, -2.55483969e-02,
             -4.77258398e-02, -6.38427394e-02, -7.06512643e-02,
             -6.61458422e-02, -5.76615888e-02, -4.64803335e-02],
            [-5.25038299e-02, -6.66129442e-02, -7.90147081e-02,
             -8.87629178e-02, -8.59653118e-02, -7.42828398e-02,
             -5.64316505e-02, -2.87083225e-02, 1.25945312e-02,
             6.19971667e-02, 8.78050260e-02, 6.19971667e-02,
             1.25945312e-02, -2.87083225e-02, -5.64316505e-02,
             -7.42828398e-02, -8.59653118e-02, -8.87629178e-02,
             -7.90147081e-02, -6.66129442e-02, -5.25038299e-02],
            [-5.69779111e-02, -7.36791817e-02, -8.97495345e-02,
             -1.04799583e-01, -1.07737239e-01, -1.02875880e-01,
             -9.46568471e-02, -7.95630162e-02, -4.96285112e-02,
             6.59954795e-03, 5.25569882e-02, 6.59954795e-03,
             -4.96285112e-02, -7.95630162e-02, -9.46568471e-02,
             -1.02875880e-01, -1.07737239e-01, -1.04799583e-01,
             -8.97495345e-02, -7.36791817e-02, -5.69779111e-02],
            [-5.90357675e-02, -7.69727119e-02, -9.48442826e-02,
             -1.12607620e-01, -1.18744885e-01, -1.18201834e-01,
             -1.17217017e-01, -1.15152899e-01, -1.09694433e-01,
             -8.82341332e-02, -1.61624035e-02, -8.82341332e-02,
             -1.09694433e-01, -1.15152899e-01, -1.17217017e-01,
             -1.18201834e-01, -1.18744885e-01, -1.12607620e-01,
             -9.48442826e-02, -7.69727119e-02, -5.90357675e-02],
            [-5.92189452e-02, -7.72680305e-02, -9.53051857e-02,
             -1.13322519e-01, -1.19770917e-01, -1.19670660e-01,
             -1.19486798e-01, -1.19092639e-01, -1.17989113e-01,
             -1.12555820e-01, -4.50009776e-02, -1.12555820e-01,
             -1.17989113e-01, -1.19092639e-01, -1.19486798e-01,
             -1.19670660e-01, -1.19770917e-01, -1.13322519e-01,
             -9.53051857e-02, -7.72680305e-02, -5.92189452e-02],
            [-5.79249958e-02, -7.51927112e-02, -9.20842554e-02,
             -1.08361430e-01, -1.12722790e-01, -1.09732675e-01,
             -1.04531672e-01, -9.44729544e-02, -7.23277773e-02,
             -2.05699911e-02, 3.58249631e-02, -2.05699911e-02,
             -7.23277773e-02, -9.44729544e-02, -1.04531672e-01,
             -1.09732675e-01, -1.12722790e-01, -1.08361430e-01,
             -9.20842554e-02, -7.51927112e-02, -5.79249958e-02],
            [-5.42527703e-02, -6.93641123e-02, -8.31684773e-02,
             -9.49114165e-02, -9.41989454e-02, -8.48645354e-02,
             -7.00894708e-02, -4.58286259e-02, -6.37563061e-03,
             4.68887998e-02, 7.77968419e-02, 4.68887998e-02,
             -6.37563061e-03, -4.58286259e-02, -7.00894708e-02,
             -8.48645354e-02, -9.41989454e-02, -9.49114165e-02,
             -8.31684773e-02, -6.93641123e-02, -5.42527703e-02],
            [-4.82490057e-02, -5.99997941e-02, -6.91786120e-02,
             -7.44891242e-02, -6.73705808e-02, -5.13001284e-02,
             -2.84188057e-02, 3.60143816e-03, 4.47470123e-02,
             8.58663851e-02, 1.04548354e-01, 8.58663851e-02,
             4.47470123e-02, 3.60143816e-03, -2.84188057e-02,
             -5.13001284e-02, -6.73705808e-02, -7.44891242e-02,
             -6.91786120e-02, -5.99997941e-02, -4.82490057e-02],
            [-4.03203010e-02, -4.79063206e-02, -5.16352259e-02,
             -4.98707253e-02, -3.67295509e-02, -1.57342058e-02,
             1.13668830e-02, 4.46551184e-02, 8.10450840e-02,
             1.11780747e-01, 1.24226598e-01, 1.11780747e-01,
             8.10450840e-02, 4.46551184e-02, 1.13668830e-02,
             -1.57342058e-02, -3.67295509e-02, -4.98707253e-02,
             -5.16352259e-02, -4.79063206e-02, -4.03203010e-02],
            [-3.10250239e-02, -3.40796094e-02, -3.22089254e-02,
             -2.37094100e-02, -5.85463114e-03, 1.77402761e-02,
             4.57786845e-02, 7.69637052e-02, 1.07537652e-01,
             1.30906328e-01, 1.39800436e-01, 1.30906328e-01,
             1.07537652e-01, 7.69637052e-02, 4.57786845e-02,
             1.77402761e-02, -5.85463114e-03, -2.37094100e-02,
             -3.22089254e-02, -3.40796094e-02, -3.10250239e-02],
            [-2.09301700e-02, -1.94475962e-02, -1.22970199e-02,
             2.07296407e-03, 2.31516868e-02, 4.74574033e-02,
             7.44743481e-02, 1.02380049e-01, 1.27776301e-01,
             1.46003379e-01, 1.52690015e-01, 1.46003379e-01,
             1.27776301e-01, 1.02380049e-01, 7.44743481e-02,
             4.74574033e-02, 2.31516868e-02, 2.07296407e-03,
             -1.22970199e-02, -1.94475962e-02, -2.09301700e-02],
            [-1.05257992e-02, -4.74329696e-03, 7.12107274e-03,
             2.63431361e-02, 4.93709790e-02, 7.31527220e-02,
             9.82233938e-02, 1.22728059e-01, 1.43894925e-01,
             1.58465026e-01, 1.63685984e-01, 1.58465026e-01,
             1.43894925e-01, 1.22728059e-01, 9.82233938e-02,
             7.31527220e-02, 4.93709790e-02, 2.63431361e-02,
             7.12107274e-03, -4.74329696e-03, -1.05257992e-02],
            [-1.89098657e-04, 9.52392382e-03, 2.54577716e-02,
             4.85730869e-02, 7.26048516e-02, 9.51726659e-02,
             1.17988523e-01, 1.39380421e-01, 1.57176612e-01,
             1.69076915e-01, 1.73274075e-01, 1.69076915e-01,
             1.57176612e-01, 1.39380421e-01, 1.17988523e-01,
             9.51726659e-02, 7.26048516e-02, 4.85730869e-02,
             2.54577716e-02, 9.52392382e-03, -1.89098657e-04],
            [9.81732797e-03, 2.30419581e-02, 4.24234701e-02,
             6.86213308e-02, 9.30164618e-02, 1.14050063e-01,
             1.34620894e-01, 1.53304069e-01, 1.68420867e-01,
             1.78321253e-01, 1.81774183e-01, 1.78321253e-01,
             1.68420867e-01, 1.53304069e-01, 1.34620894e-01,
             1.14050063e-01, 9.30164618e-02, 6.86213308e-02,
             4.24234701e-02, 2.30419581e-02, 9.81732797e-03],
            [1.93290725e-02, 3.56493099e-02, 5.79271157e-02,
             8.65611122e-02, 1.10914315e-01, 1.30317702e-01,
             1.48798006e-01, 1.65173224e-01, 1.78147031e-01,
             1.86513895e-01, 1.89408199e-01, 1.86513895e-01,
             1.78147031e-01, 1.65173224e-01, 1.48798006e-01,
             1.30317702e-01, 1.10914315e-01, 8.65611122e-02,
             5.79271157e-02, 3.56493099e-02, 1.93290725e-02],
            [2.68168937e-02, 4.52356810e-02, 6.92261217e-02,
             9.89630241e-02, 1.23093435e-01, 1.40640067e-01,
             1.56998943e-01, 1.71215219e-01, 1.82297185e-01,
             1.89360704e-01, 1.91789146e-01, 1.89360704e-01,
             1.82297185e-01, 1.71215219e-01, 1.56998943e-01,
             1.40640067e-01, 1.23093435e-01, 9.89630241e-02,
             6.92261217e-02, 4.52356810e-02, 2.68168937e-02],
            [3.19403269e-02, 5.15051953e-02, 7.61032066e-02,
             1.05705197e-01, 1.31722206e-01, 1.47466588e-01,
             1.61892450e-01, 1.74235616e-01, 1.83735386e-01,
             1.89735533e-01, 1.91788616e-01, 1.89735533e-01,
             1.83735386e-01, 1.74235616e-01, 1.61892450e-01,
             1.47466588e-01, 1.31722206e-01, 1.05705197e-01,
             7.61032066e-02, 5.15051953e-02, 3.19403269e-02],
            [3.48604070e-02, 5.49292382e-02, 7.94274234e-02,
             1.08149011e-01, 1.38923419e-01, 1.53070440e-01,
             1.65849067e-01, 1.76646162e-01, 1.84871647e-01,
             1.90029617e-01, 1.91787948e-01, 1.90029617e-01,
             1.84871647e-01, 1.76646162e-01, 1.65849067e-01,
             1.53070440e-01, 1.38923419e-01, 1.08149011e-01,
             7.94274234e-02, 5.49292382e-02, 3.48604070e-02],
            [3.53402022e-02, 5.53653759e-02, 7.91965502e-02,
             1.06486934e-01, 1.36563003e-01, 1.57713955e-01,
             1.69087164e-01, 1.78598269e-01, 1.85784340e-01,
             1.90264452e-01, 1.91787141e-01, 1.90264452e-01,
             1.85784340e-01, 1.78598269e-01, 1.69087164e-01,
             1.57713955e-01, 1.36563003e-01, 1.06486934e-01,
             7.91965502e-02, 5.53653759e-02, 3.53402022e-02],
            [3.32889822e-02, 5.28319225e-02, 7.55769079e-02,
             1.01077605e-01, 1.28592068e-01, 1.57023616e-01,
             1.71766715e-01, 1.80199729e-01, 1.86528091e-01,
             1.90454829e-01, 1.91786196e-01, 1.90454829e-01,
             1.86528091e-01, 1.80199729e-01, 1.71766715e-01,
             1.57023616e-01, 1.28592068e-01, 1.01077605e-01,
             7.55769079e-02, 5.28319225e-02, 3.32889822e-02],
            [2.87295370e-02, 4.74613283e-02, 6.88388861e-02,
             9.23568989e-02, 1.17254645e-01, 1.42483223e-01,
             1.66695764e-01, 1.81528776e-01, 1.87141877e-01,
             1.90611190e-01, 1.91785112e-01, 1.90611190e-01,
             1.87141877e-01, 1.81528776e-01, 1.66695764e-01,
             1.42483223e-01, 1.17254645e-01, 9.23568989e-02,
             6.88388861e-02, 4.74613283e-02, 2.87295370e-02],
            [2.17650266e-02, 3.94568191e-02, 5.93023344e-02,
             8.07720575e-02, 1.03124482e-01, 1.25394282e-01,
             1.46405870e-01, 1.64828303e-01, 1.79288925e-01,
             1.88553222e-01, 1.91747252e-01, 1.88553222e-01,
             1.79288925e-01, 1.64828303e-01, 1.46405870e-01,
             1.25394282e-01, 1.03124482e-01, 8.07720575e-02,
             5.93023344e-02, 3.94568191e-02, 2.17650266e-02],
            [1.25495284e-02, 2.90572166e-02, 4.72972116e-02,
             6.67423656e-02, 8.66951873e-02, 1.06290296e-01,
             1.24520131e-01, 1.40293247e-01, 1.52531693e-01,
             1.60303860e-01, 1.62970689e-01, 1.60303860e-01,
             1.52531693e-01, 1.40293247e-01, 1.24520131e-01,
             1.06290296e-01, 8.66951873e-02, 6.67423656e-02,
             4.72972116e-02, 2.90572166e-02, 1.25495284e-02],
            [1.26441934e-03, 1.65114811e-02, 3.31390978e-02,
             5.06407706e-02, 6.83765492e-02, 8.55839448e-02,
             1.01408074e-01, 1.14955639e-01, 1.25373662e-01,
             1.31946425e-01, 1.34193829e-01, 1.31946425e-01,
             1.25373662e-01, 1.14955639e-01, 1.01408074e-01,
             8.55839448e-02, 6.83765492e-02, 5.06407706e-02,
             3.31390978e-02, 1.65114811e-02, 1.26441934e-03],
            [0.00000000e+00, 2.06213867e-03, 1.71162845e-02,
             3.27888240e-02, 4.85026462e-02, 6.35932476e-02,
             7.73387997e-02, 8.90069217e-02, 9.79166934e-02,
             1.03509489e-01, 1.05416736e-01, 1.03509489e-01,
             9.79166934e-02, 8.90069217e-02, 7.73387997e-02,
             6.35932476e-02, 4.85026462e-02, 3.27888240e-02,
             1.71162845e-02, 2.06213867e-03, 0.00000000e+00]]
    )
    np.testing.assert_allclose(
        fd, fd_test, rtol=1e-5)
