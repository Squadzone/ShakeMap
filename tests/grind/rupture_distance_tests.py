import os
import sys
import numpy as np

import matplotlib.pyplot as plt

import openquake.hazardlib.geo as geo

from shakemap.grind.rupture import EdgeRupture
from shakemap.grind.rupture import QuadRupture
from shakemap.grind.origin import Origin
from shakemap.grind.sites import Sites
from shakemap.grind.distance import get_distance

homedir = os.path.dirname(os.path.abspath(__file__))  # where is this script?
shakedir = os.path.abspath(os.path.join(homedir, '..', '..'))
sys.path.insert(0, shakedir)


def test_multisegment_discordant():
    # The one thing that isn't check above is discordancy for segments
    # with multiple quads. For this, we need a synthetic example. 
    x0 = np.array([0,   1, -1, 10,   9,  7])
    y0 = np.array([0,  10, 20, 40,  35, 30])
    z0 = np.array([0,   0,  0,  0,   0,  0])
    x1 = np.array([1,  -1,  0,  9,   7,  6])
    y1 = np.array([10, 20, 30, 35,  30, 25])
    z1 = np.array([0,   0,  0,  0,   0,  0])
    x2 = np.array([3,   1,  2,  7,   5,  4])
    y2 = np.array([10, 20, 30, 35,  30, 25])
    z2 = np.array([10, 10, 10, 10,  10, 10])
    x3 = np.array([2,   3,  1,  8,   7,  5])
    y3 = np.array([0,  10, 20, 40,  35, 30])
    z3 = np.array([10, 10, 10, 10,  10, 10])

    epilat = 32.15270
    epilon = -115.30500
    proj = geo.utils.get_orthographic_projection(epilon-1, epilon+1, epilat+1, epilat-1)
    lon0,lat0 = proj(x0, y0, reverse = True)
    lon1,lat1 = proj(x1, y1, reverse = True)
    lon2,lat2 = proj(x2, y2, reverse = True)
    lon3,lat3 = proj(x3, y3, reverse = True)

    # Make an Origin object; most of the 'event' values don't matter for this example
    origin = Origin({'lat': 0,  'lon': 0, 'depth':0, 'mag': 7.2, 'id':''})
    rup = QuadRupture.fromVertices(
        lon0, lat0, z0, lon1, lat1, z1, lon2, lat2, z2, lon3, lat3, z3,
        origin, group_index = [0, 0, 0, 1, 1, 1])

    # Sites
    buf = 0.25
    lat = np.linspace(np.nanmin(rup.lats)-buf, np.nanmax(rup.lats)+buf, 20)
    lon = np.linspace(np.nanmin(rup.lons)-buf, np.nanmax(rup.lons)+buf, 20)
    lons, lats = np.meshgrid(lon, lat)
    dep = np.zeros_like(lons)
    x,y = proj(lon, lat)
    rupx,rupy = proj(rup.lons, rup.lats)
    # Calculate U and T
    dtypes = ['U', 'T']
    dists = get_distance(dtypes, lats, lons, dep, rup)

    targetU = np.array(
      [[-28.53228275, -28.36479713, -28.20139732, -28.0407734 ,
        -27.88135558, -27.72144153, -27.55935946, -27.39362017,
        -27.22300147, -27.04653062, -26.86338215, -26.67275638,
        -26.47381287, -26.26569449, -26.04762427, -25.81902477,
        -25.57961136, -25.32943282, -25.06885791, -24.79852214],
       [-23.53750292, -23.3748086 , -23.21793537, -23.06521934,
        -22.91449689, -22.76331684, -22.60928211, -22.45042208,
        -22.28542121, -22.11355532, -21.93435402, -21.74720475,
        -21.55115107, -21.34497916, -21.12749377, -20.89781118,
        -20.6555466 , -20.40086149, -20.13439948, -19.85716145],
       [-18.53499939, -18.37689929, -18.22732841, -18.08427516,
        -17.94468687, -17.80472632, -17.66045115, -17.50880802,
        -17.3484421 , -17.17963435, -17.0032098 , -16.81921732,
        -16.62638972, -16.42258419, -16.20564846, -15.9741218 ,
        -15.72753538, -15.4663671 , -15.19180844, -14.9054813 ],
       [-13.52283359, -13.36797542, -13.22589288, -13.09466537,
        -12.97028551, -12.84653536, -12.71591089, -12.57212088,
        -12.41335561, -12.24319318, -12.06681006, -11.88598424,
        -11.69798166, -11.49796348, -11.28169605, -11.04691388,
        -10.79343174, -10.52262594, -10.23677602,  -9.93851158],
       [ -8.49936685,  -8.34357094,  -8.20650964,  -8.08786858,
         -7.98403171,  -7.88628837,  -7.78005273,  -7.64833307,
         -7.48359988,  -7.29992491,  -7.11862682,  -6.94410189,
         -6.76618701,  -6.5727842 ,  -6.35634881,  -6.11465447,
         -5.84925708,  -5.56369035,  -5.26212482,  -4.94857454],
       [ -3.46638168,  -3.30047216,  -3.15914418,  -3.04618465,
         -2.96252939,  -2.90194067,  -2.84436315,  -2.75029014,
         -2.56983592,  -2.33744275,  -2.1512136 ,  -1.99833104,
         -1.84066354,  -1.6541107 ,  -1.43071517,  -1.17252753,
         -0.88592286,  -0.57817222,  -0.25582315,   0.07585567],
       [  1.56416954,   1.75393848,   1.9183586 ,   2.04909316,
          2.13723278,   2.17776584,   2.18272501,   2.20967639,
          2.37405656,   2.65073289,   2.80205222,   2.90973407,
          3.05124404,   3.2505182 ,   3.50336116,   3.7967575 ,
          4.11742779,   4.45465822,   4.80070204,   5.15033407],
       [  6.5633489 ,   6.78740885,   6.99419348,   7.17551069,
          7.31963558,   7.4113505 ,   7.43666779,   7.40177458,
          7.40517136,   7.58520044,   7.62013169,   7.71596777,
          7.90558457,   8.17213015,   8.49008681,   8.83763176,
          9.19937294,   9.56556659,   9.9305469 ,  10.29132309],
       [ 11.48996073,  11.74301446,  11.99016964,  12.22782156,
         12.44984059,  12.6446727 ,  12.78798484,  12.82584849,
         12.61992833,  12.26579742,  12.32166685,  12.54665462,
         12.86628045,  13.23578462,  13.62571822,  14.01882924,
         14.40617707,  14.78388296,  15.15089889,  15.5076165 ],
       [ 16.31383216,  16.57376544,  16.83189511,  17.08626411,
         17.33309437,  17.56429108,  17.76005623,  17.85853532,
         17.57101025,  17.32637346,  17.45075419,  17.77199513,
         18.16933168,  18.58284635,  18.9891851 ,  19.37985879,
         19.75324557,  20.11079653,  20.4549905 ,  20.78837053],
       [ 21.03975749,  21.28450315,  21.5243142 ,  21.75603974,
         21.97469496,  22.17298057,  22.34310053,  22.49668569,
         22.73940191,  22.70030633,  22.95351405,  23.35967832,
         23.75891016,  24.14867803,  24.51536915,  24.85878249,
         25.18398203,  25.49615514,  25.79932964,  26.09638269],
       [ 25.70484089,  25.92709225,  26.14280395,  26.35119497,
         26.55363501,  26.75827099,  26.9915523 ,  27.31779086,
         27.77993211,  27.71070831,  28.13624949,  28.723482  ,
         29.25285078,  29.66404032,  30.00169474,  30.30044315,
         30.57916576,  30.84804427,  31.1126134 ,  31.37586841],
       [ 30.35406633,  30.5585145 ,  30.75843356,  30.95627127,
         31.15811912,  31.3763124 ,  31.63114968,  31.94156189,
         32.23691802,  32.38759301,  32.86915665,  33.83467935,
         34.46125278,  34.89905345,  35.25111257,  35.55095664,
         35.82150686,  36.07720619,  36.32643896,  36.57385362],
       [ 35.0222379 ,  35.21734711,  35.41081942,  35.60589495,
         35.80774808,  36.02313791,  36.25826988,  36.51619168,
         36.81025966,  37.21777129,  37.86674108,  38.66578072,
         39.25203723,  39.78060643,  40.20815617,  40.5606039 ,
         40.86634527,  41.14457482,  41.40732554,  41.66197722],
       [ 39.73046099,  39.92514041,  40.12152415,  40.32316112,
         40.5350467 ,  40.76393316,  41.01937758,  41.3172128 ,
         41.68596492,  42.16604148,  42.77622755,  43.447503  ,
         44.03771478,  44.55012468,  45.00551259,  45.40376857,
         45.75505135,  46.07204699,  46.36554362,  46.64361367],
       [ 44.4876174 ,  44.68959464,  44.89710008,  45.11420443,
         45.34646809,  45.60143197,  45.88932906,  46.22363997,
         46.61975585,  47.0884227 ,  47.62307543,  48.1913408 ,
         48.74937117,  49.26945799,  49.74327902,  50.17123158,
         50.55810895,  50.91098842,  51.23731582,  51.54375617],
       [ 49.29279265,  49.50696882,  49.73006999,  49.96625305,
         50.22080319,  50.50022572,  50.81209441,  51.1642666 ,
         51.56290694,  52.00913021,  52.49553006,  53.00565389,
         53.51861282,  54.01614414,  54.48672101,  54.9254339 ,
         55.33212663,  55.70951516,  56.06170563,  56.39317058],
       [ 54.13906629,  54.3671694 ,  54.60643024,  54.86053563,
         55.13377911,  55.43088558,  55.75658576,  56.1148189 ,
         56.50752978,  56.93329478,  57.38640012,  57.85715119,
         58.33367994,  58.80451404,  59.26065475,  59.69644542,
         60.10938419,  60.49940252,  60.86803179,  61.21767916],
       [ 59.01741908,  59.25887491,  59.51248349,  59.78119592,
         60.06816694,  60.37651862,  60.70895927,  61.0672529 ,
         61.45160192,  61.86010542,  62.28853397,  62.73062937,
         63.17894547,  63.62598375,  64.06523791,  64.49185106,
         64.90281064,  65.2967858 ,  65.67377362,  66.03469546],
       [ 63.9193099 ,  64.17236414,  64.4376317 ,  64.71732366,
         65.01362255,  65.32847988,  65.66334836,  66.0188704 ,
         66.39457546,  66.7886684 ,  67.19800022,  67.61828012,
         68.04451487,  68.47157851,  68.89476917,  69.31022713,
         69.71515194,  70.10782673,  70.4875021 ,  70.85420436]]
    )
    np.testing.assert_allclose(targetU, dists['U'], atol=0.01)
    targetT = np.array(
      [[ -2.27427469e+01,  -1.97498544e+01,  -1.67512900e+01,
         -1.37464632e+01,  -1.07350712e+01,  -7.71715083e+00,
         -4.69305811e+00,  -1.66336318e+00,   1.37131605e+00,
          4.41047613e+00,   7.45381136e+00,   1.05011799e+01,
          1.35524779e+01,   1.66074913e+01,   1.96657949e+01,
          2.27267294e+01,   2.57894503e+01,   2.88530154e+01,
          3.19164798e+01,   3.49789747e+01],
       [ -2.30778766e+01,  -2.00896906e+01,  -1.70950973e+01,
         -1.40931667e+01,  -1.10834219e+01,  -8.06600712e+00,
         -5.04171582e+00,  -2.01179123e+00,   1.02248614e+00,
          4.06025218e+00,   7.10129626e+00,   1.01459367e+01,
          1.31946312e+01,   1.62475702e+01,   1.93044511e+01,
          2.23644788e+01,   2.54265185e+01,   2.84892997e+01,
          3.15515954e+01,   3.46123426e+01],
       [ -2.33971472e+01,  -2.04144525e+01,  -1.74245193e+01,
         -1.44256870e+01,  -1.14169177e+01,  -8.39830615e+00,
         -5.37141115e+00,  -2.33902937e+00,   6.95823925e-01,
          3.73133431e+00,   6.76769593e+00,   9.80663091e+00,
          1.28500821e+01,   1.58991008e+01,   1.89534737e+01,
          2.20119662e+01,   2.50728111e+01,   2.81341606e+01,
          3.11943854e+01,   3.42522163e+01],
       [ -2.36965870e+01,  -2.07206976e+01,  -1.77370901e+01,
         -1.47426715e+01,  -1.17347885e+01,  -8.71247709e+00,
         -5.67801094e+00,  -2.63761285e+00,   4.00625914e-01,
          3.43182302e+00,   6.45782532e+00,   9.48491128e+00,
          1.25187545e+01,   1.55616657e+01,   1.86127822e+01,
          2.16694756e+01,   2.47286680e+01,   2.77876297e+01,
          3.08443066e+01,   3.38973527e+01],
       [ -2.39698399e+01,  -2.10022612e+01,  -1.80281475e+01,
         -1.50423801e+01,  -1.20388157e+01,  -9.01204040e+00,
         -5.96160398e+00,  -2.89867328e+00,   1.52194374e-01,
          3.17268218e+00,   6.17334725e+00,   9.17699572e+00,
          1.21964990e+01,   1.52330975e+01,   1.82821226e+01,
          2.13375815e+01,   2.43943933e+01,   2.74490375e+01,
          3.04994435e+01,   3.35446330e+01],
       [ -2.42070742e+01,  -2.12471979e+01,  -1.82855675e+01,
         -1.53163304e+01,  -1.23296744e+01,  -9.31127857e+00,
         -6.24535210e+00,  -3.12882361e+00,  -2.24460581e-02,
          2.95354485e+00,   5.89215412e+00,   8.86387424e+00,
          1.18748249e+01,   1.49128245e+01,   1.79640055e+01,
          2.10182501e+01,   2.40696313e+01,   2.71153177e+01,
          3.01543919e+01,   3.31869788e+01],
       [ -2.43971375e+01,  -2.14368866e+01,  -1.84826148e+01,
         -1.55321207e+01,  -1.25786621e+01,  -9.60654678e+00,
         -6.58612151e+00,  -3.48118311e+00,  -3.16555025e-01,
          2.61618307e+00,   5.53740540e+00,   8.52666510e+00,
          1.15623361e+01,   1.46149780e+01,   1.76674294e+01,
          2.07125025e+01,   2.37483764e+01,   2.67756033e+01,
          2.97955606e+01,   3.28097430e+01],
       [ -2.45384925e+01,  -2.15583842e+01,  -1.85874288e+01,
         -1.56290738e+01,  -1.26867853e+01,  -9.76140655e+00,
         -6.84407754e+00,  -3.90089971e+00,  -8.41806596e-01,
          2.14754495e+00,   5.18583472e+00,   8.26271822e+00,
          1.13266091e+01,   1.43684333e+01,   1.73916223e+01,
          2.04017469e+01,   2.34034936e+01,   2.64002111e+01,
          2.93941282e+01,   3.23866586e+01],
       [ -2.46576775e+01,  -2.16355610e+01,  -1.86129545e+01,
         -1.55919156e+01,  -1.25763765e+01,  -9.57306672e+00,
         -6.59044329e+00,  -3.62352541e+00,  -5.92041388e-01,
          2.33255341e+00,   5.29498494e+00,   8.24834463e+00,
          1.11833819e+01,   1.41167617e+01,   1.70571082e+01,
          2.00065102e+01,   2.29645946e+01,   2.59302937e+01,
          2.89023967e+01,   3.18797332e+01],
       [ -2.48161623e+01,  -2.17489533e+01,  -1.86651328e+01,
         -1.55589864e+01,  -1.24224388e+01,  -9.24466730e+00,
         -6.01521475e+00,  -2.75148770e+00,   3.89519039e-01,
          2.99589525e+00,   5.45696689e+00,   8.01247078e+00,
          1.07291540e+01,   1.35565782e+01,   1.64461360e+01,
          1.93723515e+01,   2.23222250e+01,   2.52881249e+01,
          2.82650171e+01,   3.12494172e+01],
       [ -2.50857405e+01,  -2.20002811e+01,  -1.88926336e+01,
         -1.57550887e+01,  -1.25770789e+01,  -9.34497451e+00,
         -6.04430316e+00,  -2.67290100e+00,   5.40854953e-01,
          2.30509492e+00,   3.58183843e+00,   6.23701436e+00,
          9.28727128e+00,   1.23205706e+01,   1.53428945e+01,
          1.83666035e+01,   2.13934954e+01,   2.44218171e+01,
          2.74496472e+01,   3.04757209e+01],
       [ -2.55082697e+01,  -2.24454912e+01,  -1.93710045e+01,
         -1.62824768e+01,  -1.31767102e+01,  -1.00469827e+01,
         -6.86985653e+00,  -3.54681638e+00,   1.07062999e-01,
          3.34891657e-01,  -1.70694750e-01,   3.57896940e+00,
          7.17013928e+00,   1.05232789e+01,   1.37976070e+01,
          1.70230221e+01,   2.02076136e+01,   2.33576919e+01,
          2.64794914e+01,   2.95785985e+01],
       [ -2.60778515e+01,  -2.30695744e+01,  -2.00684150e+01,
         -1.70790651e+01,  -1.41074315e+01,  -1.11587507e+01,
         -8.23273307e+00,  -5.33306966e+00,  -2.80144302e+00,
         -1.84760416e+00,  -1.05368779e+00,   1.26163211e+00,
          4.90086292e+00,   8.53883059e+00,   1.20996577e+01,
          1.55589098e+01,   1.89237978e+01,   2.22114952e+01,
          2.54390313e+01,   2.86203790e+01],
       [ -2.67537229e+01,  -2.38123298e+01,  -2.08964272e+01,
         -1.80168638e+01,  -1.51896230e+01,  -1.24401995e+01,
         -9.81536176e+00,  -7.41008520e+00,  -5.38073414e+00,
         -3.78262975e+00,  -2.29669890e+00,  -3.53057240e-01,
          3.13642477e+00,   6.97021789e+00,   1.07026969e+01,
          1.42945488e+01,   1.77655640e+01,   2.11406146e+01,
          2.44409375e+01,   2.76832489e+01],
       [ -2.74832153e+01,  -2.46028623e+01,  -2.17593854e+01,
         -1.89653378e+01,  -1.62381218e+01,  -1.36022404e+01,
         -1.10914555e+01,  -8.74572618e+00,  -6.58963863e+00,
         -4.58336507e+00,  -2.57607747e+00,  -2.67233150e-01,
          2.82788692e+00,   6.36737407e+00,   9.93334021e+00,
          1.34440609e+01,   1.68846862e+01,   2.02577163e+01,
          2.35710668e+01,   2.68337230e+01],
       [ -2.82199728e+01,  -2.53838486e+01,  -2.25869234e+01,
         -1.98388981e+01,  -1.71512612e+01,  -1.45365893e+01,
         -1.20059297e+01,  -9.56220853e+00,  -7.18799023e+00,
         -4.83006994e+00,  -2.39120744e+00,   2.51308627e-01,
          3.17331949e+00,   6.33022626e+00,   9.61428455e+00,
          1.29426788e+01,   1.62705993e+01,   1.95770961e+01,
          2.28539081e+01,   2.60992146e+01],
       [ -2.89332200e+01,  -2.61222251e+01,  -2.33461951e+01,
         -2.06105222e+01,  -1.79200485e+01,  -1.52776479e+01,
         -1.26817390e+01,  -1.01225741e+01,  -7.57801870e+00,
         -5.01122873e+00,  -2.37434916e+00,   3.78303328e-01,
          3.27093827e+00,   6.29527723e+00,   9.41912399e+00,
          1.26046423e+01,   1.58204753e+01,   1.90448689e+01,
          2.22643265e+01,   2.54712657e+01],
       [ -2.96082809e+01,  -2.68067500e+01,  -2.40331802e+01,
         -2.12894659e+01,  -1.85760763e+01,  -1.58910124e+01,
         -1.32284735e+01,  -1.05774862e+01,  -7.92111801e+00,
         -5.23724922e+00,  -2.50179068e+00,   3.05790568e-01,
          3.19666197e+00,   6.16975035e+00,   9.21353475e+00,
          1.23109519e+01,   1.54443017e+01,   1.85982825e+01,
          2.17611016e+01,   2.49243957e+01],
       [ -3.02420504e+01,  -2.74395034e+01,  -2.46578094e+01,
         -2.18967353e+01,  -1.91546206e+01,  -1.64278219e+01,
         -1.37101816e+01,  -1.09927140e+01,  -8.26378719e+00,
         -5.51007519e+00,  -2.71836365e+00,   1.22111758e-01,
          3.01754598e+00,   5.96851903e+00,   8.97043180e+00,
          1.20150997e+01,   1.50927299e+01,   1.81935916e+01,
          2.13090724e+01,   2.44321477e+01],
       [ -3.08377073e+01,  -2.80281994e+01,  -2.52335334e+01,
         -2.24524366e+01,  -1.96825082e+01,  -1.69199811e+01,
         -1.41595768e+01,  -1.13945492e+01,  -8.61701306e+00,
         -5.81861191e+00,  -2.99148017e+00,  -1.29317230e-01,
          2.77170749e+00,   5.71249079e+00,   8.69110042e+00,
          1.17033684e+01,   1.47437429e+01,   1.78061436e+01,
          2.08846464e+01,   2.39739290e+01]]
    )
    np.testing.assert_allclose(targetT, dists['T'], atol=0.01)



def test_EdgeRupture_vs_QuadRupture():
    # Sites stuff
    sites = Sites.fromCenter(-122.15, 37.15, 1.5, 1.5, 0.01, 0.01)
    sm_dict = sites._GeoDict
    west = sm_dict.xmin
    east = sm_dict.xmax
    south = sm_dict.ymin
    north = sm_dict.ymax
    nx = sm_dict.nx
    ny = sm_dict.ny
    lats = np.linspace(north, south, ny)
    lons = np.linspace(west, east, nx)
    lon, lat = np.meshgrid(lons, lats)
    dep = np.zeros_like(lon)

    # Construct QuadRupture
    xp0 = np.array([-122.0, -122.5])
    yp0 = np.array([37.1, 37.4])
    xp1 = np.array([-121.7, -122.3])
    yp1 = np.array([37.2, 37.2])
    zp = np.array([0, 6])
    widths = np.array([30, 20])
    dips = np.array([30, 40])

    origin = Origin({'lat': 0,  'lon': 0, 'depth':0, 'mag': 7.2, 'id':''})
    qrup = QuadRupture.fromTrace(xp0, yp0, xp1, yp1, zp, widths, dips, origin)
    rrup_q = qrup.computeRrup(lon, lat, dep)
    rjb_q = qrup.computeRjb(lon, lat, dep)

    # Construct equivalent EdgeRupture
    toplons = np.array([-122.0, -121.7, -122.5, -122.3])
    toplats = np.array([37.1, 37.2, 37.4, 37.2])
    topdeps = np.array([0, 0, 6, 6])
    botlons = np.array([-121.886864, -121.587568, -122.635467, -122.435338])
    botlats = np.array([36.884527, 36.984246, 37.314035,  37.114261])
    botdeps = np.array([15.0000, 14.9998, 18.8558, 18.8559])
    group_index = [0, 0, 1, 1]

    erup = EdgeRupture.fromArrays(
        toplons, toplats, topdeps, botlons, botlats, botdeps,
        origin, group_index)
    rrup_e = erup.computeRrup(lon, lat, dep)
    rjb_e = erup.computeRjb(lon, lat, dep)

    # Check that QuadRupture and EdgeRupture give the same result
    # (we check the absolute values of QuadRupture elsewhere)
    np.testing.assert_allclose(rrup_e, rrup_q, atol=0.35)
    np.testing.assert_allclose(rjb_e, rjb_q, atol=0.35)


    # For ploting
    #plt.imshow(rjb_q, interpolation="none")
    #plt.imshow(rjb_e, interpolation="none")

    #fig = plt.contourf(lon, lat, rrup_e,
    #                   levels = range(0, 100, 1),
    #                   cmap=plt.cm.spectral)
    #cbar = plt.colorbar(fig)
    #for q in qrup.getQuadrilaterals():
    #    x = [a.longitude for a in q]+[q[0].longitude]
    #    y = [a.latitude for a in q]+[q[0].latitude]
    #    plt.plot(x, y, 'r')


if __name__ == "__main__":
    test_multisegment_discordant()
    test_EdgeRupture_vs_QuadRupture()
