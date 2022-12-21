#!/usr/bin/env python
import pandas as pd
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, TableColumn, DataTable, Div, FactorRange
from bokeh.models.widgets import AutocompleteInput
from bokeh.layouts import column, row

import pika
import sys
import ssl
import requests
import re;
import json
from datetime import datetime

import configparser
datos = pd.DataFrame(columns=['index', 'timestamp', 'reliability', 'speed', 'result'])
raw_datas = dict()
predictors = ['ID V10', 'ID V11', 'ID V12', 'ID V13', 'ID V14', 'ID V15', 'ID V16', 'ID V17', 'ID V2', 'ID V3', 'ID V4', 'ID V5', 'ID V6', 'ID V7', 'ID V8', 'ID V9', 'CA V1RealMaximo 1', 'CA V1RealMaximo 2', 'CA V1RealMaximo 3', 'CA V1RealMaximo 4', 'CA V1RealMaximo 5', 'CA V1RealMaximo 6', 'CA V1RealMaximo 7', 'CA V1RealMaximo 8', 'CA V1RealMaximo 9', 'CA V1RealMaximo 10', 'CA V1RealMaximo 11', 'CA V1RealMaximo 12', 'CA V1RealMedio 1', 'CA V1RealMedio 2', 'CA V1RealMedio 3', 'CA V1RealMedio 4', 'CA V1RealMedio 5', 'CA V1RealMedio 6', 'CA V1RealMedio 7', 'CA V1RealMedio 8', 'CA V1RealMedio 9', 'CA V1RealMedio 10', 'CA V1RealMedio 11', 'CA V1RealMedio 12', 'CA V1RealMinimo 1', 'CA V1RealMinimo 2', 'CA V1RealMinimo 3', 'CA V1RealMinimo 4', 'CA V1RealMinimo 5', 'CA V1RealMinimo 6', 'CA V1RealMinimo 7', 'CA V1RealMinimo 8', 'CA V1RealMinimo 9', 'CA V1RealMinimo 10', 'CA V1RealMinimo 11', 'CA V1RealMinimo 12', 'CA V2RealMaximo 1', 'CA V2RealMaximo 2', 'CA V2RealMaximo 3', 'CA V2RealMaximo 4', 'CA V2RealMaximo 5', 'CA V2RealMaximo 6', 'CA V2RealMaximo 7', 'CA V2RealMaximo 8', 'CA V2RealMaximo 9', 'CA V2RealMaximo 10', 'CA V2RealMaximo 11', 'CA V2RealMaximo 12', 'CA V2RealMedio 1', 'CA V2RealMedio 2', 'CA V2RealMedio 3', 'CA V2RealMedio 4', 'CA V2RealMedio 5', 'CA V2RealMedio 6', 'CA V2RealMedio 7', 'CA V2RealMedio 8', 'CA V2RealMedio 9', 'CA V2RealMedio 10', 'CA V2RealMedio 11', 'CA V2RealMedio 12', 'CA V2RealMinimo 1', 'CA V2RealMinimo 2', 'CA V2RealMinimo 3', 'CA V2RealMinimo 4', 'CA V2RealMinimo 5', 'CA V2RealMinimo 6', 'CA V2RealMinimo 7', 'CA V2RealMinimo 8', 'CA V2RealMinimo 9', 'CA V2RealMinimo 10', 'CA V2RealMinimo 11', 'CA V2RealMinimo 12', 'CM Activo 1', 'CM Ok 1', 'CM RealMaximo 1', 'CM RealMedio 1', 'CM RealMinimo 1', 'CJ ActivoV1 20', 'CJ ActivoV2 20', 'CJ Ok 20', 'CJ V1Ok 20', 'CJ V1RealMaximo 1', 'CJ V1RealMaximo 4', 'CJ V1RealMaximo 7', 'CJ V1RealMaximo 10', 'CJ V1RealMaximo 11', 'CJ V1RealMaximo 12', 'CJ V1RealMaximo 13', 'CJ V1RealMaximo 16', 'CJ V1RealMaximo 17', 'CJ V1RealMaximo 18', 'CJ V1RealMaximo 19', 'CJ V1RealMaximo 20', 'CJ V1RealMaximo 22', 'CJ V1RealMaximo 23', 'CJ V1RealMaximo 25', 'CJ V1RealMaximo 28', 'CJ V1RealMaximo 31', 'CJ V1RealMaximo 34', 'CJ V1RealMaximo 49', 'CJ V1RealMaximo 50', 'CJ V1RealMaximo 51', 'CJ V1RealMaximo 52', 'CJ V1RealMedio 1', 'CJ V1RealMedio 4', 'CJ V1RealMedio 7', 'CJ V1RealMedio 10', 'CJ V1RealMedio 11', 'CJ V1RealMedio 12', 'CJ V1RealMedio 13', 'CJ V1RealMedio 16', 'CJ V1RealMedio 17', 'CJ V1RealMedio 18', 'CJ V1RealMedio 19', 'CJ V1RealMedio 20', 'CJ V1RealMedio 22', 'CJ V1RealMedio 23', 'CJ V1RealMedio 25', 'CJ V1RealMedio 28', 'CJ V1RealMedio 31', 'CJ V1RealMedio 34', 'CJ V1RealMedio 49', 'CJ V1RealMedio 50', 'CJ V1RealMedio 51', 'CJ V1RealMedio 52', 'CJ V1RealMinimo 1', 'CJ V1RealMinimo 4', 'CJ V1RealMinimo 7', 'CJ V1RealMinimo 10', 'CJ V1RealMinimo 11', 'CJ V1RealMinimo 12', 'CJ V1RealMinimo 13', 'CJ V1RealMinimo 16', 'CJ V1RealMinimo 17', 'CJ V1RealMinimo 18', 'CJ V1RealMinimo 19', 'CJ V1RealMinimo 20', 'CJ V1RealMinimo 22', 'CJ V1RealMinimo 23', 'CJ V1RealMinimo 25', 'CJ V1RealMinimo 28', 'CJ V1RealMinimo 31', 'CJ V1RealMinimo 34', 'CJ V1RealMinimo 49', 'CJ V1RealMinimo 50', 'CJ V1RealMinimo 51', 'CJ V1RealMinimo 52', 'CJ V2Ok 20', 'CJ V2RealMaximo 1', 'CJ V2RealMaximo 4', 'CJ V2RealMaximo 7', 'CJ V2RealMaximo 10', 'CJ V2RealMaximo 11', 'CJ V2RealMaximo 12', 'CJ V2RealMaximo 13', 'CJ V2RealMaximo 16', 'CJ V2RealMaximo 17', 'CJ V2RealMaximo 18', 'CJ V2RealMaximo 19', 'CJ V2RealMaximo 20', 'CJ V2RealMaximo 22', 'CJ V2RealMaximo 23', 'CJ V2RealMaximo 25', 'CJ V2RealMaximo 28', 'CJ V2RealMaximo 31', 'CJ V2RealMaximo 34', 'CJ V2RealMaximo 49', 'CJ V2RealMaximo 50', 'CJ V2RealMaximo 51', 'CJ V2RealMaximo 52', 'CJ V2RealMedio 1', 'CJ V2RealMedio 4', 'CJ V2RealMedio 7', 'CJ V2RealMedio 10', 'CJ V2RealMedio 11', 'CJ V2RealMedio 12', 'CJ V2RealMedio 13', 'CJ V2RealMedio 16', 'CJ V2RealMedio 17', 'CJ V2RealMedio 18', 'CJ V2RealMedio 19', 'CJ V2RealMedio 20', 'CJ V2RealMedio 22', 'CJ V2RealMedio 23', 'CJ V2RealMedio 25', 'CJ V2RealMedio 28', 'CJ V2RealMedio 31', 'CJ V2RealMedio 34', 'CJ V2RealMedio 49', 'CJ V2RealMedio 50', 'CJ V2RealMedio 51', 'CJ V2RealMedio 52', 'CJ V2RealMinimo 1', 'CJ V2RealMinimo 4', 'CJ V2RealMinimo 7', 'CJ V2RealMinimo 10', 'CJ V2RealMinimo 11', 'CJ V2RealMinimo 12', 'CJ V2RealMinimo 13', 'CJ V2RealMinimo 16', 'CJ V2RealMinimo 17', 'CJ V2RealMinimo 18', 'CJ V2RealMinimo 19', 'CJ V2RealMinimo 20', 'CJ V2RealMinimo 22', 'CJ V2RealMinimo 23', 'CJ V2RealMinimo 25', 'CJ V2RealMinimo 28', 'CJ V2RealMinimo 31', 'CJ V2RealMinimo 34', 'CJ V2RealMinimo 49', 'CJ V2RealMinimo 50', 'CJ V2RealMinimo 51', 'CJ V2RealMinimo 52', 'CP RealMinimo', 'CP RealMedio', 'CP RealMaximo', 'CPG RealMaximo 1', 'CPG RealMaximo 2', 'CPG RealMedio 1', 'CPG RealMedio 2', 'CPG RealMinimo 1', 'CPG RealMinimo 2', 'CS RealMaximo 1', 'CS RealMaximo 2', 'CS RealMaximo 3', 'CS RealMaximo 4', 'CS RealMaximo 5', 'CS RealMaximo 6', 'CS RealMaximo 7', 'CS RealMaximo 8', 'CS RealMaximo 9', 'CS RealMaximo 10', 'CS RealMaximo 12', 'CS RealMaximo 13', 'CS RealMaximo 14', 'CS RealMaximo 16', 'CS RealMaximo 18', 'CS RealMaximo 25', 'CS RealMaximo 26', 'CS RealMaximo 27', 'CS RealMaximo 28', 'CS RealMaximo 29', 'CS RealMaximo 30', 'CS RealMaximo 31', 'CS RealMaximo 32', 'CS RealMaximo 33', 'CS RealMaximo 34', 'CS RealMaximo 35', 'CS RealMaximo 36', 'CS RealMaximo 39', 'CS RealMaximo 40', 'CS RealMaximo 41', 'CS RealMaximo 42', 'CS RealMaximo 43', 'CS RealMaximo 44', 'CS RealMaximo 45', 'CS RealMaximo 46', 'CS RealMaximo 47', 'CS RealMaximo 48', 'CS RealMaximo 49', 'CS RealMaximo 50', 'CS RealMaximo 51', 'CS RealMaximo 52', 'CS RealMaximo 53', 'CS RealMaximo 54', 'CS RealMedio 1', 'CS RealMedio 2', 'CS RealMedio 3', 'CS RealMedio 4', 'CS RealMedio 5', 'CS RealMedio 6', 'CS RealMedio 7', 'CS RealMedio 8', 'CS RealMedio 9', 'CS RealMedio 10', 'CS RealMedio 11', 'CS RealMedio 12', 'CS RealMedio 13', 'CS RealMedio 14', 'CS RealMedio 16', 'CS RealMedio 18', 'CS RealMedio 25', 'CS RealMedio 26', 'CS RealMedio 27', 'CS RealMedio 28', 'CS RealMedio 29', 'CS RealMedio 30', 'CS RealMedio 31', 'CS RealMedio 32', 'CS RealMedio 33', 'CS RealMedio 34', 'CS RealMedio 35', 'CS RealMedio 36', 'CS RealMedio 39', 'CS RealMedio 40', 'CS RealMedio 41', 'CS RealMedio 42', 'CS RealMedio 43', 'CS RealMedio 44', 'CS RealMedio 45', 'CS RealMedio 46', 'CS RealMedio 47', 'CS RealMedio 48', 'CS RealMedio 49', 'CS RealMedio 50', 'CS RealMedio 51', 'CS RealMedio 52', 'CS RealMedio 53', 'CS RealMedio 54', 'CS RealMinimo 1', 'CS RealMinimo 2', 'CS RealMinimo 3', 'CS RealMinimo 4', 'CS RealMinimo 5', 'CS RealMinimo 6', 'CS RealMinimo 7', 'CS RealMinimo 8', 'CS RealMinimo 9', 'CS RealMinimo 10', 'CS RealMinimo 11', 'CS RealMinimo 12', 'CS RealMinimo 13', 'CS RealMinimo 14', 'CS RealMinimo 16', 'CS RealMinimo 18', 'CS RealMinimo 25', 'CS RealMinimo 26', 'CS RealMinimo 27', 'CS RealMinimo 28', 'CS RealMinimo 29', 'CS RealMinimo 30', 'CS RealMinimo 31', 'CS RealMinimo 32', 'CS RealMinimo 33', 'CS RealMinimo 34', 'CS RealMinimo 35', 'CS RealMinimo 36', 'CS RealMinimo 39', 'CS RealMinimo 40', 'CS RealMinimo 41', 'CS RealMinimo 42', 'CS RealMinimo 43', 'CS RealMinimo 44', 'CS RealMinimo 45', 'CS RealMinimo 46', 'CS RealMinimo 47', 'CS RealMinimo 48', 'CS RealMinimo 49', 'CS RealMinimo 50', 'CS RealMinimo 51', 'CS RealMinimo 52', 'CS RealMinimo 53', 'CS RealMinimo 54', 'CV V4', 'CV V5', 'CV V6', 'CV V8', 'CV V9', 'CV V11', 'CV V12']
mean_std = [(57.067109070951005, 7.827515676223898), (142.88753617403452, 123.46769723448526), (689.865931543758, 55.05560973746009), (367.826339686658, 2.3737127356225742), (464.5625436583175, 20.298239250096486), (17.263022652429896, 1.2858336072951146), (726.0943019658716, 49.87363758072738), (516.6536523301068, 38.25567618804062), (9.62738249675681, 2.124910701629002), (2139.477846522303, 119.62789663519989), (105.5294631274324, 48.2440464458043), (57.229343378904304, 13.595887475032967), (628.0897365532383, 70.47781796833226), (3.9321425007484283, 3.3707061938179113), (486.5001247380501, 33.41399852221564), (44.834871769284504, 16.4151508297742), (49.360767388484184, 8.611977345577595), (200.67470811296278, 4.7502647894423395), (196.4980291388085, 7.394225542404853), (119.75466520307354, 2.0980944424822168), (197.5416874563417, 5.600535604606492), (196.71674483584474, 5.727528133603797), (158.98178824468616, 10.139924562832071), (164.7843279113861, 8.70222533401016), (213.62137012274223, 4.30242412346166), (163.44057479293483, 7.0419697778277355), (173.361840135715, 5.270067979877132), (221.70207564115358, 5.126735471353621), (47.8843428799521, 8.519884057852021), (199.81147091108673, 4.739114294144967), (195.5687057179922, 7.391065000356801), (118.16784752020756, 1.9842249025849383), (195.9384292984732, 5.6759977902187435), (194.86929947111068, 5.86406879605157), (155.7358048098992, 9.410820101793469), (162.05705518411335, 9.02531390400836), (212.81601137611017, 4.402894188169127), (162.4676180021954, 7.128613375839454), (171.32968266640057, 5.315470681399336), (220.45826264843828, 5.278849955464012), (47.37551142600539, 8.48122855087045), (199.70888633868876, 4.758923891196874), (195.34936633070552, 7.4528438343420556), (117.63449256561222, 1.978326989097693), (195.28614908691748, 5.8310500233447495), (193.8951202474803, 6.055747894908135), (153.4951102684363, 9.994954246331687), (160.32087616006388, 9.447672245621963), (212.752644446662, 4.45147664043457), (162.35555333799022, 7.183296379164439), (170.39427202873964, 5.593848764281159), (220.1611615607225, 5.521915649178037), (992.3563516615109, 105.22355631442281), (997.3343478694741, 21.758670439328583), (1046.561919968067, 86.4507010161032), (1034.1295778864385, 28.82061971853577), (532.8041113661311, 69.92194547678297), (815.3890080830256, 63.35414235994474), (667.119723580481, 24.034160197236556), (884.8897814589362, 48.26064819572232), (647.1558726673985, 29.38741127270539), (963.4820626683963, 117.18066452358819), (816.4236104181219, 74.00557691581173), (621.557803612414, 62.0062152325576), (989.017188903303, 104.78025176060699), (993.8548548049097, 15.999960663804591), (1045.280186608123, 86.2106428181274), (1028.734108372418, 24.745414866097377), (529.4185211056781, 59.73015162709269), (806.7762698333499, 61.37614357688879), (666.2777167947311, 14.430321392881726), (875.2269484083425, 42.71655709370323), (646.5959235605229, 28.862222220652942), (960.6404550444067, 115.7118783248835), (800.0714749027043, 70.47490919820412), (616.5799820377208, 51.49151056189059), (986.9445165153178, 104.41775471659805), (992.3243438778564, 12.514911600982659), (1044.8094252070653, 86.11157693561341), (1024.3598692745236, 20.923725943414407), (527.290714499551, 50.65339098333732), (799.6439477098094, 59.23110280248901), (666.2524947610019, 14.369765843934193), (867.80266440475, 38.56981906465181), (646.4450653627382, 28.446322693856274), (958.5616954395769, 114.87696428381145), (791.4108372417923, 68.04589335758388), (613.4704121345175, 41.51034686387255), (0.9363835944516515, 0.24407139251386503), (0.9361590659614809, 0.24447241197614622), (77.26254864783954, 24.858945905414657), (77.26254864783954, 24.858945905414657), (77.26254864783954, 24.858945905414657), (0.11820177626983334, 0.322850920261438), (0.11942420916076239, 0.32429105913482814), (0.11600638658816485, 0.32023657391502725), (0.11827661909989023, 0.32293940957554595), (84.16999301466919, 5.065663355238063), (84.3827711805209, 6.535840827516933), (70.58070551841134, 6.132166887766036), (18.0215796826664, 5.1408626966333335), (12.800094800918073, 2.1629197121034855), (14.168970162658418, 3.5719517823134708), (56.54103881848119, 5.898736091069457), (18.178051092705317, 5.160435909767507), (14.894870771380102, 3.4886774113334367), (14.41507833549546, 2.214356264469141), (86.44149785450554, 8.550761988603995), (1.5612713302065662, 4.27562042404999), (67.86485879652729, 4.323925140498145), (22.69409240594751, 2.9308956765636323), (73.68057080131723, 3.987581540223509), (75.24259055982436, 4.628571282293006), (39.190824269035026, 4.1478831215806835), (62.22884442670392, 18.963396416893328), (13.196163057579083, 2.7002009638308153), (17.348543059574894, 3.066606295070558), (14.458337491268336, 2.3511943246251983), (14.984283005688056, 2.1304774509341886), (83.90976449456141, 5.057947318817176), (84.16128629877258, 6.541510912590861), (70.3348717692845, 6.103858774598765), (17.61351162558627, 5.089142546243757), (12.631324219139806, 2.160302964123398), (13.900384193194292, 3.5184646077804302), (55.3747380500948, 5.855732283203366), (17.83759105877657, 4.9625816336499), (14.73488174832851, 3.4638480557796707), (14.019359345374713, 2.090790225222396), (86.27659415228021, 8.562125424384545), (1.5258956191996806, 4.184270982154914), (67.70803811994811, 4.269049990129069), (22.188404350863188, 2.932249686757446), (73.14544456641053, 3.9752058765919265), (74.89272527691847, 4.591396851481536), (38.453522602534676, 4.076142088603585), (62.04370821275322, 18.95402546391166), (12.710033928749626, 2.485588149877407), (17.122417922363038, 2.9680344055942265), (14.354305957489272, 2.322791058472156), (14.743139407244787, 2.024802939181757), (83.90968965173137, 5.058333168101888), (84.16128629877258, 6.541510912590861), (70.3348717692845, 6.103858774598765), (17.60455543358946, 5.087893021133804), (12.631274323919769, 2.160409930481442), (13.89659215647141, 3.5234710941726273), (55.09268037122044, 5.903925846772148), (17.82149985031434, 4.947035877218419), (14.733334996507335, 3.460969582394129), (14.002270232511725, 2.0863694519258646), (86.27207863486677, 8.576662087324024), (1.5208063067558129, 4.173607165295502), (67.70372218341483, 4.265001801581486), (22.139931144596346, 2.9577779026234188), (73.14319928150883, 3.976931321876231), (74.89215148188804, 4.592277166780523), (38.377781658517115, 4.043375122059932), (62.043284103382895, 18.954773394202917), (12.703248178824468, 2.479299005926733), (17.116056281808202, 2.9602903181921434), (14.35365731962878, 2.3233516893806723), (14.735231014868775, 2.012503680508965), (0.11702923859894222, 0.3214591325463811), (518.4416974353857, 47.95343876274807), (531.8504640255463, 47.47949414881783), (463.6028091008881, 36.018817595928766), (666.4666949406247, 58.710810953765), (671.1581428999102, 52.23191270613382), (683.3060822273226, 50.290203816290756), (515.628879353358, 48.92029639911206), (695.8188304560423, 55.55438872580542), (722.8056082227323, 72.67127472789946), (697.9162009779463, 61.58923750997186), (582.3518610917074, 50.93791506390519), (60.089187705817785, 163.43973161739504), (607.9444666200978, 45.6293899151364), (538.9381798223731, 42.28389138594287), (489.94149785450554, 30.90856218651415), (452.1033330006985, 29.855719211413977), (424.28587466320727, 27.861439122766523), (381.2968017163956, 35.2455604434478), (722.6538269633769, 61.25386304892436), (673.3629128829458, 56.56134838769818), (728.3202524698133, 59.119661654210695), (714.0771380101786, 56.330381501287974), (518.0445564314939, 48.04682952665181), (530.8913531583675, 47.49213857976226), (463.31306755812795, 36.1107330156085), (664.0267937331604, 58.437278178960916), (669.477646941423, 52.21121862912898), (680.8093753118451, 50.2842526129473), (512.6812942820078, 48.852235016058714), (693.7830306356651, 55.29744433682561), (721.213127432392, 72.57151926607166), (696.2273974653228, 61.720640583551535), (581.2006286797724, 50.951024516567955), (59.91462927851512, 162.96478343864442), (607.3194541462927, 45.68580069935756), (538.0808053088514, 42.0958976356341), (488.6443468715697, 30.857489561713717), (451.61046801716395, 29.766374809031767), (422.0988424308951, 27.766209907925298), (380.6746582177427, 35.18667777990807), (720.1232910887137, 61.43847445728076), (672.3617403452749, 56.735602511084906), (726.3512124538469, 59.16073281104944), (712.5082077636962, 56.312800583958754), (518.0226025346772, 48.08022144901501), (530.7547400459036, 47.54736938190553), (463.27968765592254, 36.12607185160496), (662.3281109669693, 58.2256832460634), (668.5877656920467, 52.30305169760512), (679.1340435086319, 50.31719777860943), (510.5303861890031, 48.80666871545335), (692.5155922562618, 55.08778588083747), (720.4319678674783, 72.50966941505183), (695.347395469514, 61.88522837767999), (580.9979542959784, 51.009082019046595), (59.84814389781459, 162.78327018068353), (607.2629228619899, 45.72999446950559), (537.9045753916774, 42.03380788052144), (488.19780959984035, 30.801389717905938), (451.58809001097694, 29.73829163597367), (420.75109769484084, 27.708831631638233), (380.642126534278, 35.199606278237106), (718.4056980341284, 61.67656415883479), (671.9147789641752, 56.88595299328329), (725.2188653826963, 59.21550754622457), (711.6362388983135, 56.29375699666925), (346.6295778864385, 20.687526526203374), (369.22412932841036, 20.951719222672125), (414.36174034527494, 23.7565494930119), (709.6826664005588, 21.435689833969935), (965.7424907693843, 25.307042960694847), (653.9742540664604, 13.43747045056423), (830.5713252170442, 16.15905051617898), (603.9475351761301, 22.531947600835796), (764.3926504340884, 16.63324524295467), (206.5298622891927, 8.02473419660888), (172.37616006386588, 20.971979444633657), (240.80862688354455, 14.631121957368787), (173.01584173236205, 6.7303181098770475), (187.94616305757907, 18.453385896253742), (189.63167348568007, 27.498819368660605), (51.11273824967568, 3.2635697945730358), (43.35762398962179, 4.427446979659618), (197.05373715198084, 13.11287402760902), (39.262947809599844, 7.497600893779853), (161.39457140005987, 7.519694403715579), (202.96686957389483, 7.861720630273708), (200.80513421814192, 9.373646685584077), (212.0258207763696, 14.238445674189176), (192.37364035525397, 8.91969650070728), (64.72852010777368, 7.159781718825497), (53.512598543059575, 5.998583267394972), (57.638833449755516, 9.135414004524211), (56.049246582177425, 15.372709756424365), (35.332177427402456, 3.6220889576855133), (149.4531483883844, 13.48820104071172), (42.40759405248977, 6.57108221924528), (148.96519808402354, 12.082154443103567), (38.02998702724279, 3.3917514848822297), (35.08449755513422, 2.888875740353739), (88.22013771080731, 4.883937240775046), (82.2813092505738, 10.052696466957531), (164.70946013371918, 7.622502642431457), (124.3409090909091, 8.082842774120225), (195.093428799521, 25.45972442457912), (168.19890729468116, 12.882149743184387), (152.50653627382496, 8.651913476410268), (163.91415527392476, 12.001733369784118), (135.0297375511426, 17.694916231662454), (55.116655024448654, 3.6876341789186573), (32.80478495160164, 3.8151845456594082), (88.85976948408343, 16.645935336983065), (49.298772577587066, 10.802209055109726), (150.89038020157668, 31.678107433954356), (169.81266839636763, 11.437101165170906), (172.38796028340485, 21.148407536327053), (169.1743338988125, 13.71371055601503), (171.57164953597444, 14.019004090030386), (186.45965971459935, 5.554823840866947), (151.3767089112863, 18.77391244054405), (222.0231763297076, 19.820549042313125), (156.1583175331803, 4.46842274293805), (171.9717094102385, 16.961479519862415), (182.60952000798324, 27.182936976146028), (46.44943119449157, 3.120553856898678), (39.266141103682266, 4.389736366004191), (190.14621794232113, 12.916109580717277), (34.02514719089911, 7.449942977384412), (228.97136014369823, 6.997109188576069), (147.84667198882346, 6.594569949510229), (190.6675232012773, 6.774608420796819), (178.4060473006686, 7.803407974284742), (185.5151431992815, 12.214287878671277), (168.65337790639657, 8.0593036075341), (59.15836742840036, 6.736605209664567), (48.69509031034827, 5.6279491544505245), (52.754764993513625, 8.636923403155293), (51.062019758507134, 14.33619294421052), (31.43136912483784, 3.38888248884129), (137.70569304460633, 12.594654777467348), (37.602858996108175, 6.701893270498432), (145.2615507434388, 11.892949796887516), (35.71400059874264, 3.278106870351201), (31.335370721484882, 2.550698962929187), (81.26344676180022, 4.7028085765032195), (75.32272228320527, 9.206346247578814), (156.56299271529787, 7.383540917550905), (118.92450853208263, 7.655601021437065), (184.9555184113362, 24.36223801404543), (159.74054485580282, 12.462916743402056), (146.7798622891927, 8.177922407925962), (156.8515866679972, 11.43281158234021), (127.93690749426204, 16.85011687247884), (51.8969663706217, 3.532409955479761), (31.241193493663307, 3.7747301510276126), (83.8519608821475, 15.733349815972778), (46.92326115158168, 10.409563095998255), (146.3914529488075, 30.21833691537639), (160.66794731064763, 10.945941994723565), (163.39047999201676, 20.126216637563278), (159.86186508332503, 13.140462692486556), (162.32773675281908, 13.419603574798254), (164.73465721983834, 7.383983321665796), (141.78956690949008, 17.75101041638541), (209.3293583474703, 20.244066147466217), (138.527617004291, 5.932825968260757), (152.77068156870573, 15.690754859606189), (177.22575092306158, 27.44827559690135), (41.98153876858597, 3.2457047268556223), (35.4774972557629, 4.404941008644888), (184.92805109270532, 13.409706763950195), (29.073819978046103, 7.35330650797168), (215.19042510727473, 7.363320159756129), (132.28647340584772, 7.212021778695851), (172.05994910687556, 7.84504100502576), (166.80466021355153, 9.265119490622531), (159.95766390579783, 10.930031463656713), (145.76666500349268, 7.291049970297674), (53.62426404550444, 6.474362707777073), (44.00456541263347, 5.30743851949205), (47.7164454645245, 8.035076905197258), (46.16398064065463, 12.979835934590236), (27.97482786149087, 3.741676060649788), (123.73922263247181, 12.040805280231597), (33.17390978944217, 7.361878670692951), (141.94850813292086, 12.249843724585201), (33.34949106875561, 3.262902532195186), (27.965472507733757, 2.5531899425201843), (73.64339886238898, 5.047554075393928), (68.0011725376709, 8.573424265992292), (144.23370921065762, 7.963944352695739), (101.71502345075342, 6.66098174561992), (168.5640654625287, 22.43213922459599), (146.82918371420018, 12.566148028096372), (131.48418321524798, 7.37528000735896), (133.2531433988624, 10.23772806172697), (118.45017962279213, 15.96612459751087), (47.84532481788245, 3.5119698798487833), (29.9496058277617, 3.9590190569285895), (76.83232711306258, 14.269787177775878), (42.40168146891528, 9.489551155658942), (138.56915477497256, 28.140964114825067), (146.32057678874364, 10.508132158503974), (149.13536573196288, 18.716042193797392), (144.85849715597246, 12.53967920327652), (147.80945015467518, 12.816277980400477), (24.174197234806908, 4.895879008818716), (27.713559991517812, 5.447014379195437), (55.939528185809806, 11.585766256273129), (26.81226397565113, 5.608020534978584), (55.42284373440775, 11.471502665185351), (40.85363143648338, 15.12337056049895), (598.8079410363237, 230.5696268924786)]
mean_std = list(zip(predictors, mean_std))
id_mostrar = AutocompleteInput(title="Elige id para mostrar", completions=[], value = '', width=300)

def push(json_data: dict, datos_hist: pd.DataFrame) -> pd.DataFrame:
    global datos
    global raw_datas
    """
    Push data to a dataframe
    """

    index = json_data['id']
    timestamp = json_data['timestamp'][:-1]
    reliability = round(float(json_data['payload'][0]['value']),2)
    speed_timestamp = round(float(datetime.strptime(json_data['prediction_timestamp'],'%Y-%m-%dT%H:%M:%S.%fZ').timestamp() - datetime.strptime(json_data['timestamp'],'%Y-%m-%dT%H:%M:%S.%fZ').timestamp()), 2)
    result = json_data['result']['label']
    raw_data = pd.DataFrame(json_data['raw_data'], index=[0])
    raw_data = raw_data.loc[:, raw_data.columns.isin(predictors)]
    raw_datas[index] = raw_data

    new_data = pd.DataFrame([[index, timestamp, reliability, speed_timestamp, result]], columns=datos.columns)
    # concat the new data to the old data
    datos = pd.concat([datos_hist, new_data], ignore_index=True)


config = configparser.ConfigParser()

config.read("./config.ini")

LOCALHOST = config["MESSAGEBUS"]["LOCALHOST"]
SERVER = config["MESSAGEBUS"]["SERVER"]
PORT = config["MESSAGEBUS"]["PORT"]
USERNAME = config["MESSAGEBUS"]["USERNAME"]
PASSWORD = config["MESSAGEBUS"]["PASSWORD"]
CA_CERT = config["MESSAGEBUS"]["CA_CERT"]

EXCHANGE = config["MESSAGEBUS"]["EXCHANGE"]
ROUTING_KEY = config["MESSAGEBUS"]["ROUTING_KEY_OUTPUT"]
try:
    if CA_CERT!='':
        context = ssl.create_default_context(cafile=CA_CERT)
        context.check_hostname=False
        context.verify_mode = ssl.VerifyMode.CERT_NONE
        ssl_options = pika.SSLOptions(context, LOCALHOST)
        credentials = pika.PlainCredentials(USERNAME, PASSWORD)
        conn_params = pika.ConnectionParameters(host=SERVER,
                            port=PORT,
                            credentials=credentials,
                                                ssl_options=ssl_options)
    else:
        credentials = pika.PlainCredentials(USERNAME, PASSWORD)
        conn_params = pika.ConnectionParameters(host=SERVER,
                    port=PORT,
                    credentials=credentials)
    connection = pika.BlockingConnection(conn_params)
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise

channel = connection.channel()
result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(
    exchange=EXCHANGE, queue=queue_name, routing_key=ROUTING_KEY)

print(f' [*] Waiting for logs in {ROUTING_KEY}. To exit press CTRL+C')

def create_barshow():

    """
    Crea el gráfico de barras inicial vacío
    """

    source = ColumnDataSource(data=dict(variable=[], deviation=[], raw_values=[]))
    p = figure(x_range=FactorRange(*[]), plot_height=250, title="Variables más relevantes",
           toolbar_location=None, tools="hover", tooltips="@variable: @raw_values")

    p.vbar(x='variable', top='deviation', width=0.9, source=source)
    return p, source

def update_barshow(attrname, old, new) -> None:

    """
    Actualiza el gráfico de barras con los datos de la muestra seleccionada
        - mean_std: lista con las medias y desviaciones estándar de cada variable
    """

    raw_data = raw_datas[id_mostrar.value].iloc[0]
    #calculate the deviation of each variable
    deviations = [abs((raw_data[variable] - mean)/std) for variable, (mean, std) in mean_std]
    
    #Which variables have the highest deviation
    variables = [(variable, deviation) for variable, deviation in sorted(zip(predictors, deviations), key=lambda x: x[1], reverse=True)][:5]
    variables, deviations = zip(*variables)
    raw_values = [raw_data[variable] for variable in variables]
    #creates a columndatasoruce with the variables and their deviations
    source = ColumnDataSource(data=dict(variable=variables, deviation=deviations, raw_values=raw_values))

    barshow.x_range.factors = variables
    barshow.title.text = f'Variables que más se desvían de lo normal en la muestra: {id_mostrar.value}'
    source_bar.data.update(source.data)


def create_datatable(src:ColumnDataSource,
    width:int = 400,  
    height:int = 600, 
    widthColumns:int = 100,
    ) -> DataTable:

    """
    Crea un DataTable con los datos de la fuente de datos   
    """
    def reliability_formatter(value):
        if value < 0.1:
            return f'<span style="color: red">{value}</span>'
        return value

    columns = []
    columns.append(TableColumn(field="index", title="id", width=widthColumns))
    columns.append(TableColumn(field="reliability", title="reliability", width=widthColumns, formatter = reliability_formatter))
    columns.append(TableColumn(field="timestamp", title="timestamp", width=widthColumns))
    columns.append(TableColumn(field="speed", title="prediction (s)", width=widthColumns))

    tabla = DataTable(sortable = True, reorderable = True, 
                autosize_mode='none', source=src,
                columns=columns, index_position = None, 
                width = width, height = height)

    return tabla
    
    
def update():
    """
    Actualiza el DataTable con los datos nuevos
    """
    
    method, properties, body = channel.basic_get(queue=queue_name, auto_ack=True)
    
    if body:
        # Process the message
        push(json.loads(json.loads(body)), datos)
        
        tabla.source.data = dict(datos)
        id_mostrar.completions = datos['index'].unique().tolist()

tabla = create_datatable(ColumnDataSource(datos))
barshow, source_bar = create_barshow()
controls = [id_mostrar]
for control in controls:
    control.on_change('value', update_barshow)
    
curdoc().add_root(row(column(Div(text="""<h1>Resultados en Streaming</h1>""", width=500), tabla, width=500), column(id_mostrar, barshow, width=500)))
curdoc().title = "Aplicación ZDMP"
curdoc().add_periodic_callback(update, 1000 * 15)
