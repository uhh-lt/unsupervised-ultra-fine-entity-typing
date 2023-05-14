import jobimtext_handler
import random
import json
import stanza
import inflect


def test_get_senses_from_jobimtext():
    # selected random 5 sample mentions for each cluster type (e.g. 200,200)
    # and one sense for each to test in 'test_jobimtext_handler.ipynb'
    # ['the insulation', 'Sollom', 'Marcille', 'Today', 'British Airways'] for 200,200
    # 6, 0, 11, 7, 0 -- indexes for the randomly selected senses, respectively to the mention
    # ['the Greens', 'Lee Teng-hui', 'Scotch Whisky', 'Spencer', 'trumpet'] for 50,50
    # 14, 18, 1, 17, 9 -- indexes for the randomly selected senses, respectively to the mention
    # ['the liver', 'Lynyrd Skynyrd', 'the outside', 'Olympic National Park', 'CEO'] for 200,50
    # 1, 7, 3, 2, 1 -- indexes for the randomly selected senses, respectively to the mention

    response_200_0 = jobimtext_handler.get_senses_from_jobimtext(mention='the insulation', cluster_type='200,200')
    response_200_1 = jobimtext_handler.get_senses_from_jobimtext(mention='Sollom', cluster_type='200,200')
    response_200_2 = jobimtext_handler.get_senses_from_jobimtext(mention='Marcille', cluster_type='200,200')
    response_200_3 = jobimtext_handler.get_senses_from_jobimtext(mention='Today', cluster_type='200,200')
    response_200_4 = jobimtext_handler.get_senses_from_jobimtext(mention='British Airways', cluster_type='200,200')

    response_50_0 = jobimtext_handler.get_senses_from_jobimtext(mention='the Greens', cluster_type='50,50')
    response_50_1 = jobimtext_handler.get_senses_from_jobimtext(mention='Lee Teng-hui', cluster_type='50,50')
    response_50_2 = jobimtext_handler.get_senses_from_jobimtext(mention='Scotch Whisky', cluster_type='50,50')
    response_50_3 = jobimtext_handler.get_senses_from_jobimtext(mention='Spencer', cluster_type='50,50')
    response_50_4 = jobimtext_handler.get_senses_from_jobimtext(mention='trumpet', cluster_type='50,50')

    response_20050_0 = jobimtext_handler.get_senses_from_jobimtext(mention='the liver', cluster_type='200,50')
    response_20050_1 = jobimtext_handler.get_senses_from_jobimtext(mention='Lynyrd Skynyrd', cluster_type='200,50')
    response_20050_2 = jobimtext_handler.get_senses_from_jobimtext(mention='the outside', cluster_type='200,50')
    response_20050_3 = jobimtext_handler.get_senses_from_jobimtext(mention='Olympic National Park',
                                                                   cluster_type='200,50')
    response_20050_4 = jobimtext_handler.get_senses_from_jobimtext(mention='CEO', cluster_type='200,50')

    # test-1: select random one sense and check manually
    # -- 200,200 -- #
    assert response_200_0[6]['cui'] == str(6)
    # list is from http://ltmaggie.informatik.uni-hamburg.de/jobimviz/#
    # search for 'the insulation#MWE' and select 200,200 cluster, get the sense 6 and by copying manually
    assert response_200_0[6]['senses'] == ['the liner#MWE', 'the duct#MWE', 'the coil#MWE',
                                           'the piping#MWE', 'the plug#MWE',
                                           'the pipe#MWE', 'the connector#MWE', 'the jacket#MWE',
                                           'the shell#MWE', 'the tube#MWE',
                                           'the separator#MWE', 'the cylinder#MWE',
                                           'the sleeve#MWE', 'the diaphragm#MWE',
                                           'the radiator#MWE', 'the piston#MWE',
                                           'the conduit#MWE', 'the bag#MWE',
                                           'the valve#MWE', 'the heater#MWE',
                                           '^the sock#MWE', '^the bellows#MWE',
                                           '^the shield#MWE', '^some duct#MWE',
                                           '^in the liner#MWE', '^the paper bag#MWE']
    assert response_200_0[6]['isas'] == ['thing:176', 'component:110', 'time:75', 'item:64', 'case:45', 'stuff:30']

    assert response_200_1[0]['cui'] == str(0)
    # list is from http://ltmaggie.informatik.uni-hamburg.de/jobimviz/#
    # search for 'Sollom#NN' and select 200,200 cluster, get the sense 0 and by copying manually
    assert response_200_1[0]['senses'] == ['Iacopino#NN', 'Sirkin#NN', 'Donaghue#NN', 'Huskey#NN', 'Reisner#NN',
                                           'Litvin#NN', 'PHR#NN']
    assert response_200_1[0]['isas'] == []

    assert response_200_2[11]['cui'] == str(11)
    # list is from http://ltmaggie.informatik.uni-hamburg.de/jobimviz/#
    # search for 'Marcille#NN' and select 200,200 cluster, get the sense 11 and by copying manually
    assert response_200_2[11]['senses'] == ['Bergman#NN', 'Rossellini#NN', 'Isabella Rossellini#Per']
    assert response_200_2[11]['isas'] == ['director:528', 'filmmaker:94', 'film:70', 'name:66', 'masters:60',
                                          'luminary:39', 'artist:36', 'star:34']

    assert response_200_3[7]['cui'] == str(7)
    # list is from http://ltmaggie.informatik.uni-hamburg.de/jobimviz/#
    # search for 'Today#NN' and select 200,200 cluster, get the sense 7 and by copying manually
    assert response_200_3[7]['senses'] == ['World Today#MWE', '^World today#MWE', '^The World Today#MWE']
    assert response_200_3[7]['isas'] == []

    assert response_200_4[0]['cui'] == str(0)
    # list is from http://ltmaggie.informatik.uni-hamburg.de/jobimviz/#
    # search for 'British Airways#MWE' and select 200,200 cluster, get the sense 0 and by copying manually
    # since there are many, I checked first 64
    assert response_200_4[0]['senses'][0:64] == ['Airways#NN', 'Air France#MWE', 'Lufthansa#NN', 'British Airways#Org',
                                                 'KLM#NN', 'Alitalia#NN', 'Qantas#NN', 'Aeroflot#NN',
                                                 'Air Canada#MWE', 'Iberia#NN', 'American Airlines#MWE',
                                                 'Finnair#NN', 'Ryanair#NN', 'Virgin Atlantic#MWE',
                                                 'Etihad#NN', 'Airlines#NN', 'Lufthansa#Org',
                                                 'Singapore Airlines#MWE', 'Emirates#NN', 'Aer Lingus#MWE',
                                                 'US Airways#MWE', 'Air Berlin#MWE', 'JAL#NN', 'Cathay Pacific#MWE',
                                                 'China Eastern#MWE', 'Delta#NN', 'Lingus#NN', 'United Airlines#MWE',
                                                 'Qantas#Org', 'Cathay#NN', 'Royal Jordanian#MWE', 'KLM#Org',
                                                 'China Southern#MWE', 'Air China#MWE', 'Japan Airlines#MWE',
                                                 'Qatar Airways#MWE', 'JetBlue#NN', 'Jet Airways#MWE',
                                                 'Air New Zealand#MWE', 'Austrian#NN', 'Turkish#NN',
                                                 'American Airlines#Org', 'Air Lines#MWE', 'Air France#Org',
                                                 'Germanwings#NN', 'SAS#NN', 'all Nippon#MWE', 'Alaska Airlines#MWE',
                                                 'Asiana#NN', 'China Airlines#MWE', 'Qatar#NN', 'Delta Air Lines#MWE',
                                                 'Korean Air#MWE', 'Alitalia#Org', 'Delta#Org',
                                                 'Southwest Airlines#MWE', 'Swiss#NN', 'Delta Airlines#MWE',
                                                 'Air Canada#Org', 'Air India#MWE', 'Ryanair#Org', 'Etihad Airways#MWE',
                                                 'Virgin Australia#MWE', 'US Airways#Org']
    assert response_200_4[0]['isas'] == ['airline:57380481', 'carrier:15220323', 'company:6417360', 'country:5866728',
                                         'airport:2538228', 'place:1191936', 'world:980320', 'brand:965004',
                                         'Airlines:825344', 'number:746338', 'partner:587328', 'city:451440',
                                         'client:392424', 'day:296090', 'market:290640', 'customer:282780',
                                         'nation:251910', 'Europe:236700']

    # -- 50,50 -- #

    assert response_50_0[14]['cui'] == str(14)
    # list is from http://ltmaggie.informatik.uni-hamburg.de/jobimviz/#
    # search for 'the Greens#MWE' and select 50,50 cluster, get the sense 14 and by copying manually
    assert response_50_0[14]['senses'] == ['the Communists#MWE', 'Communists#NN', '^Bolsheviks#Org', '^Marxists#NN',
                                           '^Commies#NN', '^Revolutionaries#NN', '^the Marxists#MWE']
    assert response_50_0[14]['isas'] == ['group:2838', 'everyone:1056', 'party:996', 'leftist:489', 'radical:387',
                                         'revolutionary:264', 'people:252', 'socialist:222', 'left:141', 'opponent:122',
                                         'enemy:93', 'ideology:84', 'element:81', 'activist:81', 'Democrats:72',
                                         'subversive:66', 'government:66', 'totalitarians:66']

    assert response_50_1[18]['cui'] == str(18)
    # list is from http://ltmaggie.informatik.uni-hamburg.de/jobimviz/#
    # search for 'Lee Teng-hui#MWE' and select 50,50 cluster, get the sense 18 and by copying manually
    assert response_50_1[18]['senses'] == ['Hugo Chavez#MWE', 'Chavez#NN', 'Hugo Chavez#Per', 'Chavez#Per', 'Chávez#NN']
    assert response_50_1[18]['isas'] == ['leader:4855', 'people:4430', 'dictator:4160', 'someone:2220', 'guy:1920',
                                         'thug:975', 'tyrant:930', 'demagogue:900', 'man:820', 'figure:510',
                                         'despot:460', 'folk:410', 'government:395', 'country:392', 'leftist:335',
                                         'People:328', 'president:320', 'politician:280']

    assert response_50_2[1]['cui'] == str(1)
    # list is from http://ltmaggie.informatik.uni-hamburg.de/jobimviz/#
    # search for 'Scotch Whisky#MWE' and select 50,50 cluster, get the sense 1 and by copying manually
    assert response_50_2[1]['senses'] == ['Macallan#NN', 'Talisker#NN', 'Glenlivet#NN', 'Glenfiddich#NN',
                                          'Laphroaig#NN', 'Bowmore#NN', 'Ardbeg#NN', 'Islay#NN', 'Balvenie#NN',
                                          'Glenmorangie#NN', 'Speyside#NN', 'Lagavulin#NN', 'Ila#NN', 'Springbank#NN',
                                          'Chivas Regal#MWE', 'Glenfarclas#NN', 'Bruichladdich#NN', 'Caol Ila#MWE',
                                          'Aberlour#NN', 'the Macallan#MWE', 'Auchentoshan#NN', 'Bunnahabhain#NN',
                                          'Clynelish#NN', 'Cragganmore#NN', 'Dalmore#NN', 'Glenmorangie#Org',
                                          'the Glenlivet#MWE', 'Rosebank#NN', 'Glenrothes#NN', 'Oban#NN', 'Chivas#NN',
                                          'Glendronach#NN', 'Pulteney#NN', 'Glengoyne#NN', 'Mortlach#NN',
                                          'Highland Park#MWE', 'Ledaig#NN', 'Bruichladdich#Per', 'Macallan#Org',
                                          '^Amrut#NN', '^Balblair#NN', '^Talisker#Loc', '^Cardhu#NN',
                                          '^Old Pulteney#MWE', '^Lagavulin#Loc', 'Isle of Skye#MWE',
                                          '^Royal Salute#MWE', '^Kavalan#NN', '^Dalwhinnie#NN', '^Longmorn#NN',
                                          '^Glen Grant#Per', '^Bowmore#Per', '^Linkwood#NN', '^Port Ellen#MWE',
                                          '^Kilchoman#NN', '^Caperdonich#NN', '^Nikka#NN', '^Penderyn#NN',
                                          '^Edradour#NN', '^the Glenrothes#MWE', '^GlenDronach#NN',
                                          '^Glen Grant#MWE', '^Lagavulin#Org', '^Dufftown#NN', '^Benriach#NN',
                                          '^Benromach#NN', '^Pure Malt#MWE', '^Glenkinchie#NN', '^Hakushu#NN',
                                          '^speyside#NN', '^Longrow#NN', '^BenRiach#NN', '^Glenturret#NN',
                                          '^Bladnoch#NN', '^Caol Ila#Per', '^Laphroiag#NN', '^J&B#NN',
                                          '^Laphroig#NN', '^Springbank#Org', '^Benrinnes#NN', '^cask-strength#NN',
                                          '^Hazelburn#NN', '^Auchroisk#NN', '^Talisker#Org', '^Ardbeg#Org',
                                          '^Isle of Islay#MWE', '^Caol#NN', '^Linkwood#Org', '^ardbeg#NN',
                                          '^Cardhu#Per']
    assert response_50_2[1]['isas'] == ['distillery:28764', 'malt:15211', 'whisky:11655', 'brand:9962',
                                        'name:4872', 'bottle:1456', 'Scotch whisky:1273', 'area:1089',
                                        'scotches:1064', 'place:996', 'dram:720', 'Smells:672', 'Islay:672',
                                        'islands:603', 'Scotches:598', 'one:576', 'Islay malt:539']

    assert response_50_3[17]['cui'] == str(17)
    # list is from http://ltmaggie.informatik.uni-hamburg.de/jobimviz/#
    # search for 'Spencer#NN' and select 50,50 cluster, get the sense 17 and by copying manually
    assert response_50_3[17]['senses'] == ['Hanna#NN', 'Aria#NN', '^Vdara#NN', '^Aria#Org']
    assert response_50_3[17]['isas'] == ['Dwellers:472', 'hotel:390', 'manga:240', 'name:208', 'place:108',
                                         'Hotels:108', 'people:93', 'girl:93', 'brand:90', 'shows:88', 'stuff:87',
                                         'peace:84', 'character:75', 'Kalos Queen:72', 'lot:72', 'series:64',
                                         'thing:63', 'restaurant:60', 'town:60']

    assert response_50_4[9]['cui'] == str(9)
    # list is from http://ltmaggie.informatik.uni-hamburg.de/jobimviz/#
    # search for 'trumpet#NN' and select 50,50 cluster, get the sense 9 and by copying manually
    assert response_50_4[9]['senses'] == ['trumpet player#MWE', 'trumpeter#NN', 'jazz trumpeter#MWE',
                                          'jazz trumpet#MWE', '^Trumpeter#NN', '^the trumpeter#MWE',
                                          '^Trumpet player#MWE', '^jazz man#MWE', '^Trumpeters#NN',
                                          '^jazz Trumpeter#MWE', '^american jazz trumpeter#MWE',
                                          '^trumpeteer#NN', '^trumpeter-composer#NN', '^trumpeter/composer#NN',
                                          '^cornet player#MWE', '^jazz Trumpet#MWE', '^american jazz musician#MWE',
                                          '^Bix#NN', '^trumpetist#NN', '^flugelhornist#NN']
    assert response_50_4[9]['isas'] == ['musician:138', 'sound:30']

    # -- 200,50 -- #
    assert response_20050_0[1]['cui'] == str(1)
    # list is from http://ltmaggie.informatik.uni-hamburg.de/jobimviz/#
    # search for 'the liver#MWE' and select 200,50 cluster, get the sense 1 and by copying manually
    assert response_20050_0[1]['senses'] == ['a liver#MWE', 'by the liver#MWE', 'a kidney#MWE', 'a lung#MWE',
                                             'thyroid#DT', 'the pancreatic#MWE', '^a stomach#MWE',
                                             '^in the breast#MWE', '^the corneal#MWE', '^the gastric#MWE',
                                             '^the ovarian#MWE', '^the cancer#MWE', '^adipose#DT',
                                             '^a bladder#MWE', '^a colon#MWE', '^a prostate#MWE', '^a skin#MWE',
                                             '^the placental#MWE', '^a breast#MWE', '^by the kidney#MWE',
                                             '^a ovarian#MWE', '^all lung#MWE', '^the gingival#MWE', '^tendon#DT',
                                             '^a colorectal#MWE', '^from the breast#MWE', '^a sinus#MWE',
                                             '^the ovarian cancer#MWE', '^some breast#MWE', '^all breast#MWE',
                                             '^a urinary tract#MWE', '^glomerular filtration#MWE', '^some prostate#MWE']
    assert response_20050_0[1]['isas'] == ['tissue:8064', 'organ:1332', 'body:891', 'thing:774', 'condition:471',
                                           'structure:422', 'disease:381', 'cancer:300', 'part:176', 'variety:141',
                                           'stuff:120', 'area:112', 'system:102', 'lot:98', 'neck:96', 'range:84',
                                           'body tissue:81', 'application:74', 'ailment:70']

    assert response_20050_1[7]['cui'] == str(7)
    # list is from http://ltmaggie.informatik.uni-hamburg.de/jobimviz/#
    # search for 'Lynyrd Skynyrd#MWE' and select 200,50 cluster, get the sense 7 and by copying manually
    assert response_20050_1[7]['senses'] == ['Goo Goo Dolls#MWE', '^Counting Crows#MWE', '^Third Eye Blind#MWE',
                                             '^Goo Goo Dolls#Org', '^the Counting Crows#MWE']
    assert response_20050_1[7]['isas'] == ['band:1144', 'act:764', 'artist:632', 'group:196', 'star:156',
                                           'Tampa theme park:124', 'name:88', 'rocker:72', 'rock:56', 'stuff:52',
                                           'Bands:48', 'performer:48', 'song:45',
                                           'music:36', 'sound:30', 'lot:30', 'rock band:30']

    assert response_20050_2[3]['cui'] == str(3)
    # list is from http://ltmaggie.informatik.uni-hamburg.de/jobimviz/#
    # search for 'the outside#MWE' and select 200,50 cluster, get the sense 3 and by copying manually
    assert response_20050_2[3]['senses'] == ['the side#MWE', 'side#NN', 'upper part#MWE', 'lower part#MWE',
                                             'on top#MWE', 'left side#MWE', 'opposite side#MWE', 'both side#MWE',
                                             'the right side#MWE', 'on the side#MWE', 'of the side#MWE',
                                             'right side#MWE', 'top half#MWE', 'lower half#MWE', 'the other side#MWE',
                                             'other side#MWE', 'all side#MWE', 'on bottom#MWE', 'upper half#MWE',
                                             'two side of#MWE', 'bottom half#MWE', 'both end#MWE',
                                             'the bottom half#MWE', 'of each side#MWE', 'the left-hand side#MWE',
                                             'hand side#MWE', 'on the plate#MWE', 'the left#MWE', 'three side#MWE',
                                             'right part#MWE', 'on side#MWE', 'other end#MWE', 'wrong side#MWE',
                                             'right half#MWE', 'two half#MWE', 'far side#MWE', 'the far side#MWE',
                                             'the same side#MWE', '^each half#MWE', '^any side#MWE',
                                             'the top corner#MWE', '^left half#MWE', '^left end#MWE',
                                             '^which side#MWE', '^left-hand side#MWE', '^to a side#MWE',
                                             '^the far left#MWE', '^leave side#MWE', '^on edge#MWE', '^left part#MWE',
                                             '^on a side#MWE', '^right on top#MWE', '^leave corner#MWE',
                                             '^leave part#MWE', '^short end#MWE', '^near side#MWE', '^no side#MWE',
                                             '^the far leave#MWE', '^some side#MWE', '^the leave#MWE', '^otherside#JJ',
                                             '^which end#MWE', '^leave portion#MWE']

    assert response_20050_2[3]['isas'] == ['i:3712', 'thing:3208', 'place:2568', 'time:2365', 'lot:2310', 'Seems:2200',
                                           'area:2115', 'side:1824', 'body:1344', 'detail:1216', 'people:668',
                                           'war:606', 'everything:594', 'feature:546', 'face:535', 'look:520',
                                           'part:516', 'country:484', 'game:475']

    assert response_20050_3[2]['cui'] == str(2)
    # list is from http://ltmaggie.informatik.uni-hamburg.de/jobimviz/#
    # search for 'Olympic National Park#MWE' and select 200,50 cluster, get the sense 2 and by copying manually
    assert response_20050_3[2]['senses'] == ['National Historical Park#MWE', 'Historical Park#MWE', 'Historic Park#MWE',
                                             'National Historic Park#MWE', 'Harpers Ferry#MWE']
    assert response_20050_3[2]['isas'] == ['site:36']

    assert response_20050_4[1]['cui'] == str(1)
    # list is from http://ltmaggie.informatik.uni-hamburg.de/jobimviz/#
    # search for 'CEO#NN' and select 200,50 cluster, get the sense 1 and by copying manually
    assert response_20050_4[1]['senses'] == ['founder and CEO#MWE', 'co-founder#NN', 'cofounder#NN', 'Co-founder#NN',
                                             'Founder and CEO#MWE', 'founder and chief#MWE', 'Co-Founder#NN',
                                             'co-founder and chief#MWE', 'company founder#MWE', 'founder/ceo#NN',
                                             'co-founder and former#MWE', 'founder and Chief#MWE', 'Cofounder#NN',
                                             'Company founder#MWE', '^Internet entrepreneur#MWE', '^Founder/CEO#NN',
                                             '^founder and former#MWE', '^co-founder and Chief#MWE',
                                             '^serial entrepreneur#MWE', '^CEO/Founder#NN', '^Founder and Chief#MWE',
                                             '^the entrepreneur#MWE', '^CEO/founder#NN', '^founder and ceo#MWE',
                                             '^co-founder and executive#MWE', '^Co-Founders#NN', '^co-founder#JJ',
                                             '^Co-founder and Chief#MWE', '^Board and Chief#MWE',
                                             '^owner and chief#MWE', '^co-founder and Executive#MWE',
                                             '^founder and Executive#MWE', '^web entrepreneur#MWE',
                                             '^Co-Founder and Executive#MWE']
    assert response_20050_4[1]['isas'] == ['key Lexra employee:440', 'people:336', 'employee:250', 'family:180',
                                           'investor:124', 'hat:123', 'executive:123', 'staff:84', 'management team:68',
                                           'woman:64', 'member:64', 'speaker:60', 'entrepreneur:60',
                                           'management veteran:56', 'Indians:56', 'figure:52',
                                           'management:48', 'group:42', 'collaboration tool:40', 'team:40']
    ########################################
    # test-2: check the number of senses and the number of terms in each sense

    # the number of senses checked manually from http://ltmaggie.informatik.uni-hamburg.de/jobimviz/#
    # search for 'the insulation#MWE' and select 200,200 cluster, there are 11 senses
    assert len(response_200_0) == 11
    # from the same search, after the name of sense (e.g. Sense 0) there is a number
    # showing the number of terms
    assert len(response_200_0[0]['senses']) == 98
    assert len(response_200_0[1]['senses']) == 12
    assert len(response_200_0[2]['senses']) == 78
    assert len(response_200_0[3]['senses']) == 17
    assert len(response_200_0[4]['senses']) == 14
    assert len(response_200_0[5]['senses']) == 79
    assert len(response_200_0[6]['senses']) == 26
    assert len(response_200_0[7]['senses']) == 30
    assert len(response_200_0[8]['senses']) == 12
    assert len(response_200_0[9]['senses']) == 3
    assert len(response_200_0[10]['senses']) == 25

    # the number of senses checked manually from http://ltmaggie.informatik.uni-hamburg.de/jobimviz/#
    # search for 'Sollom#NN' and select 200,200 cluster, there are 1 senses
    assert len(response_200_1) == 1
    # from the same search, after the name of sense (e.g. Sense 0) there is a number
    # showing the number of terms
    assert len(response_200_1[0]['senses']) == 7

    # the number of senses checked manually from http://ltmaggie.informatik.uni-hamburg.de/jobimviz/#
    # search for 'Marcille#NN'and select 200,200 cluster, there are 14 senses
    assert len(response_200_2) == 14
    # from the same search, after the name of sense (e.g. Sense 0) there is a number
    # showing the number of terms
    assert len(response_200_2[0]['senses']) == 73
    assert len(response_200_2[1]['senses']) == 6
    assert len(response_200_2[2]['senses']) == 10
    assert len(response_200_2[3]['senses']) == 14
    assert len(response_200_2[4]['senses']) == 6
    assert len(response_200_2[5]['senses']) == 3
    assert len(response_200_2[6]['senses']) == 6
    assert len(response_200_2[7]['senses']) == 14
    assert len(response_200_2[8]['senses']) == 18
    assert len(response_200_2[9]['senses']) == 3
    assert len(response_200_2[10]['senses']) == 55
    assert len(response_200_2[11]['senses']) == 3
    assert len(response_200_2[12]['senses']) == 3
    assert len(response_200_2[13]['senses']) == 3

    # the number of senses checked manually from http://ltmaggie.informatik.uni-hamburg.de/jobimviz/#
    # search for 'Today#NN' and select 200,200 cluster, there are 10 senses
    assert len(response_200_3) == 10
    # from the same search, after the name of sense (e.g. Sense 0) there is a number
    # showing the number of terms
    assert len(response_200_3[0]['senses']) == 188
    assert len(response_200_3[1]['senses']) == 51
    assert len(response_200_3[2]['senses']) == 12
    assert len(response_200_3[3]['senses']) == 6
    assert len(response_200_3[4]['senses']) == 33
    assert len(response_200_3[5]['senses']) == 5
    assert len(response_200_3[6]['senses']) == 3
    assert len(response_200_3[7]['senses']) == 3
    assert len(response_200_3[8]['senses']) == 7
    assert len(response_200_3[9]['senses']) == 15

    # the number of senses checked manually from http://ltmaggie.informatik.uni-hamburg.de/jobimviz/#
    # search for 'British Airways#MWE' and select 200,200 cluster, there are 13 senses
    assert len(response_200_4) == 1
    # from the same search, after the name of sense (e.g. Sense 0) there is a number
    # showing the number of terms
    assert len(response_200_4[0]['senses']) == 1349

    # the number of senses checked manually from http://ltmaggie.informatik.uni-hamburg.de/jobimviz/#
    # search for 'the Greens#MWE' and select 50,50 cluster, there are 25 senses
    assert len(response_50_0) == 25
    # from the same search, after the name of sense (e.g. Sense 0) there is a number
    # showing the number of terms
    assert len(response_50_0[0]['senses']) == 79
    assert len(response_50_0[1]['senses']) == 24
    assert len(response_50_0[2]['senses']) == 64
    assert len(response_50_0[3]['senses']) == 7
    assert len(response_50_0[4]['senses']) == 36
    assert len(response_50_0[5]['senses']) == 3
    assert len(response_50_0[6]['senses']) == 6
    assert len(response_50_0[7]['senses']) == 7
    assert len(response_50_0[8]['senses']) == 13
    assert len(response_50_0[9]['senses']) == 3
    assert len(response_50_0[10]['senses']) == 22
    assert len(response_50_0[11]['senses']) == 21
    assert len(response_50_0[12]['senses']) == 13
    assert len(response_50_0[13]['senses']) == 13
    assert len(response_50_0[14]['senses']) == 7
    assert len(response_50_0[15]['senses']) == 5
    assert len(response_50_0[16]['senses']) == 10
    assert len(response_50_0[17]['senses']) == 4
    assert len(response_50_0[18]['senses']) == 7
    assert len(response_50_0[19]['senses']) == 10
    assert len(response_50_0[20]['senses']) == 30
    assert len(response_50_0[21]['senses']) == 6
    assert len(response_50_0[22]['senses']) == 3
    assert len(response_50_0[23]['senses']) == 4
    assert len(response_50_0[24]['senses']) == 8

    # the number of senses checked manually from http://ltmaggie.informatik.uni-hamburg.de/jobimviz/#
    # search for 'Lee Teng-hui#MWE' and select 50,50 cluster, there are 20 senses
    assert len(response_50_1) == 20
    # from the same search, after the name of sense (e.g. Sense 0) there is a number
    # showing the number of terms
    assert len(response_50_1[0]['senses']) == 5
    assert len(response_50_1[1]['senses']) == 4
    assert len(response_50_1[2]['senses']) == 3
    assert len(response_50_1[3]['senses']) == 19
    assert len(response_50_1[4]['senses']) == 5
    assert len(response_50_1[5]['senses']) == 9
    assert len(response_50_1[6]['senses']) == 3
    assert len(response_50_1[7]['senses']) == 9
    assert len(response_50_1[8]['senses']) == 4
    assert len(response_50_1[9]['senses']) == 13
    assert len(response_50_1[10]['senses']) == 5
    assert len(response_50_1[11]['senses']) == 36
    assert len(response_50_1[12]['senses']) == 3
    assert len(response_50_1[13]['senses']) == 46
    assert len(response_50_1[14]['senses']) == 5
    assert len(response_50_1[15]['senses']) == 4
    assert len(response_50_1[16]['senses']) == 3
    assert len(response_50_1[17]['senses']) == 4
    assert len(response_50_1[18]['senses']) == 5
    assert len(response_50_1[19]['senses']) == 3

    # the number of senses checked manually from http://ltmaggie.informatik.uni-hamburg.de/jobimviz/#
    # search for 'Scotch Whisky#MWE' and select 50,50 cluster, there are 7 senses
    assert len(response_50_2) == 7
    # from the same search, after the name of sense (e.g. Sense 0) there is a number
    # showing the number of terms
    assert len(response_50_2[0]['senses']) == 137
    assert len(response_50_2[1]['senses']) == 90
    assert len(response_50_2[2]['senses']) == 57
    assert len(response_50_2[3]['senses']) == 4
    assert len(response_50_2[4]['senses']) == 4
    assert len(response_50_2[5]['senses']) == 21
    assert len(response_50_2[6]['senses']) == 12

    # the number of senses checked manually from http://ltmaggie.informatik.uni-hamburg.de/jobimviz/#
    # search for 'Spencer#NN' and select 50,50 cluster, there are 21 senses
    assert len(response_50_3) == 21
    # from the same search, after the name of sense (e.g. Sense 0) there is a number
    # showing the number of terms
    assert len(response_50_3[0]['senses']) == 7
    assert len(response_50_3[1]['senses']) == 3
    assert len(response_50_3[2]['senses']) == 18
    assert len(response_50_3[3]['senses']) == 10
    assert len(response_50_3[4]['senses']) == 4
    assert len(response_50_3[5]['senses']) == 3
    assert len(response_50_3[6]['senses']) == 10
    assert len(response_50_3[7]['senses']) == 3
    assert len(response_50_3[8]['senses']) == 48
    assert len(response_50_3[9]['senses']) == 6
    assert len(response_50_3[10]['senses']) == 26
    assert len(response_50_3[11]['senses']) == 3
    assert len(response_50_3[12]['senses']) == 4
    assert len(response_50_3[13]['senses']) == 41
    assert len(response_50_3[14]['senses']) == 126
    assert len(response_50_3[15]['senses']) == 33
    assert len(response_50_3[16]['senses']) == 10
    assert len(response_50_3[17]['senses']) == 4
    assert len(response_50_3[18]['senses']) == 4
    assert len(response_50_3[19]['senses']) == 7
    assert len(response_50_3[20]['senses']) == 5

    # the number of senses checked manually from http://ltmaggie.informatik.uni-hamburg.de/jobimviz/#
    # search for 'trumpet#NN' and select 50,50 cluster, there are 13 senses
    assert len(response_50_4) == 13
    # from the same search, after the name of sense (e.g. Sense 0) there is a number
    # showing the number of terms
    assert len(response_50_4[0]['senses']) == 131
    assert len(response_50_4[1]['senses']) == 28
    assert len(response_50_4[2]['senses']) == 104
    assert len(response_50_4[3]['senses']) == 36
    assert len(response_50_4[4]['senses']) == 158
    assert len(response_50_4[5]['senses']) == 6
    assert len(response_50_4[6]['senses']) == 24
    assert len(response_50_4[7]['senses']) == 46
    assert len(response_50_4[8]['senses']) == 88
    assert len(response_50_4[9]['senses']) == 20
    assert len(response_50_4[10]['senses']) == 35
    assert len(response_50_4[11]['senses']) == 30
    assert len(response_50_4[12]['senses']) == 15

    # the number of senses checked manually from http://ltmaggie.informatik.uni-hamburg.de/jobimviz/#
    # search for 'the liver#MWE' and select 200,50 cluster, there are 14 senses
    assert len(response_20050_0) == 14
    # from the same search, after the name of sense (e.g. Sense 0) there is a number
    # showing the number of terms
    assert len(response_20050_0[0]['senses']) == 282
    assert len(response_20050_0[1]['senses']) == 33
    assert len(response_20050_0[2]['senses']) == 31
    assert len(response_20050_0[3]['senses']) == 16
    assert len(response_20050_0[4]['senses']) == 19
    assert len(response_20050_0[5]['senses']) == 12
    assert len(response_20050_0[6]['senses']) == 20
    assert len(response_20050_0[7]['senses']) == 46
    assert len(response_20050_0[8]['senses']) == 3
    assert len(response_20050_0[9]['senses']) == 17
    assert len(response_20050_0[10]['senses']) == 16
    assert len(response_20050_0[11]['senses']) == 7
    assert len(response_20050_0[12]['senses']) == 11
    assert len(response_20050_0[13]['senses']) == 31

    # the number of senses checked manually from http://ltmaggie.informatik.uni-hamburg.de/jobimviz/#
    # search for 'Lynyrd Skynyrd#MWE' and select 200,50 cluster, there are 8 senses
    assert len(response_20050_1) == 8
    # from the same search, after the name of sense (e.g. Sense 0) there is a number
    # showing the number of terms
    assert len(response_20050_1[0]['senses']) == 200
    assert len(response_20050_1[1]['senses']) == 228
    assert len(response_20050_1[2]['senses']) == 24
    assert len(response_20050_1[3]['senses']) == 11
    assert len(response_20050_1[4]['senses']) == 4
    assert len(response_20050_1[5]['senses']) == 6
    assert len(response_20050_1[6]['senses']) == 3
    assert len(response_20050_1[7]['senses']) == 5

    # the number of senses checked manually from http://ltmaggie.informatik.uni-hamburg.de/jobimviz/#
    # search for 'the outside#MWE' and select 200,50 cluster, there are 14 senses
    assert len(response_20050_2) == 14
    # from the same search, after the name of sense (e.g. Sense 0) there is a number
    # showing the number of terms
    assert len(response_20050_2[0]['senses']) == 26
    assert len(response_20050_2[1]['senses']) == 11
    assert len(response_20050_2[2]['senses']) == 17
    assert len(response_20050_2[3]['senses']) == 63
    assert len(response_20050_2[4]['senses']) == 37
    assert len(response_20050_2[5]['senses']) == 25
    assert len(response_20050_2[6]['senses']) == 47
    assert len(response_20050_2[7]['senses']) == 7
    assert len(response_20050_2[8]['senses']) == 7
    assert len(response_20050_2[9]['senses']) == 3
    assert len(response_20050_2[10]['senses']) == 16
    assert len(response_20050_2[11]['senses']) == 23
    assert len(response_20050_2[12]['senses']) == 23
    assert len(response_20050_2[13]['senses']) == 7

    # the number of senses checked manually from http://ltmaggie.informatik.uni-hamburg.de/jobimviz/#
    # search for 'Olympic National Park#MWE' and select 200,50 cluster, there are 23 senses
    assert len(response_20050_3) == 23
    # from the same search, after the name of sense (e.g. Sense 0) there is a number
    # showing the number of terms
    assert len(response_20050_3[0]['senses']) == 104
    assert len(response_20050_3[1]['senses']) == 16
    assert len(response_20050_3[2]['senses']) == 5
    assert len(response_20050_3[3]['senses']) == 22
    assert len(response_20050_3[4]['senses']) == 10
    assert len(response_20050_3[5]['senses']) == 3
    assert len(response_20050_3[6]['senses']) == 11
    assert len(response_20050_3[7]['senses']) == 4
    assert len(response_20050_3[8]['senses']) == 4
    assert len(response_20050_3[9]['senses']) == 6
    assert len(response_20050_3[10]['senses']) == 6
    assert len(response_20050_3[11]['senses']) == 9
    assert len(response_20050_3[12]['senses']) == 4
    assert len(response_20050_3[13]['senses']) == 18
    assert len(response_20050_3[14]['senses']) == 15
    assert len(response_20050_3[15]['senses']) == 5
    assert len(response_20050_3[16]['senses']) == 4
    assert len(response_20050_3[17]['senses']) == 3
    assert len(response_20050_3[18]['senses']) == 3
    assert len(response_20050_3[19]['senses']) == 3
    assert len(response_20050_3[20]['senses']) == 5
    assert len(response_20050_3[21]['senses']) == 5
    assert len(response_20050_3[22]['senses']) == 6

    # the number of senses checked manually from http://ltmaggie.informatik.uni-hamburg.de/jobimviz/#
    # search for 'CEO#NN' and select 200,50 cluster, there are 17 senses
    assert len(response_20050_4) == 17
    # from the same search, after the name of sense (e.g. Sense 0) there is a number
    # showing the number of terms
    assert len(response_20050_4[0]['senses']) == 132
    assert len(response_20050_4[1]['senses']) == 34
    assert len(response_20050_4[2]['senses']) == 23
    assert len(response_20050_4[3]['senses']) == 5
    assert len(response_20050_4[4]['senses']) == 19
    assert len(response_20050_4[5]['senses']) == 45
    assert len(response_20050_4[6]['senses']) == 11
    assert len(response_20050_4[7]['senses']) == 15
    assert len(response_20050_4[8]['senses']) == 12
    assert len(response_20050_4[9]['senses']) == 3
    assert len(response_20050_4[10]['senses']) == 10
    assert len(response_20050_4[11]['senses']) == 6
    assert len(response_20050_4[12]['senses']) == 21
    assert len(response_20050_4[13]['senses']) == 3
    assert len(response_20050_4[14]['senses']) == 6
    assert len(response_20050_4[15]['senses']) == 4
    assert len(response_20050_4[16]['senses']) == 5


def test_process_jobimtext_result():
    # test-1: w/o postprocessing - randomly take some mentions and check their results with various output numbers
    # selected random 5 sample mentions and check all its senses
    # to test in 'test_jobimtext_handler.ipynb'
    # ['number one', 'Sri Lanka', 'randomness', 'Camp Morton', 'Los Angeles']
    f = open("../open_type/release/crowd/dev.json", "r")
    dev_data = [json.loads(sent.strip()) for sent in f.readlines()]
    mentions = set([mention_info['mention_span'] for mention_info in dev_data])
    results = {mention: jobimtext_handler.get_senses_from_jobimtext(mention=mention, cluster_type='200,200')
               for mention in mentions}

    # Note that: since some senses contain a lot of sense terms, 'set' is not checked
    # because I could not memorize what I see manually.
    # search for 'number one#MWE' in JoBimText -- http://ltmaggie.informatik.uni-hamburg.de/jobimviz/#
    # and manually count
    cui_0 = results['number one'][0]
    sense_list = cui_0['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 183
    isas_list = cui_0['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 19
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_0,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_1 = results['number one'][1]
    sense_list = cui_1['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 15
    isas_list = cui_1['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 20
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_1,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_2 = results['number one'][2]
    sense_list = cui_2['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 1
    isas_list = cui_2['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 14
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_2,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    # search for 'Sri Lanka#MWE' in JoBimText --
    # http://ltmaggie.informatik.uni-hamburg.de/jobimviz/#  and manually count
    cui_0 = results['Sri Lanka'][0]
    sense_list = cui_0['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 189
    isas_list = cui_0['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 18
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_0,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_1 = results['Sri Lanka'][1]
    sense_list = cui_1['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 3
    isas_list = cui_1['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 14
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_1,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_2 = results['Sri Lanka'][2]
    sense_list = cui_2['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 2
    isas_list = cui_2['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 10
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_2,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_3 = results['Sri Lanka'][3]
    sense_list = cui_3['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 3
    isas_list = cui_3['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 19
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_3,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    # search for 'randomness#NN' in JoBimText
    # -- http://ltmaggie.informatik.uni-hamburg.de/jobimviz/#  and manually count
    cui_0 = results['randomness'][0]
    sense_list = cui_0['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 55
    isas_list = cui_0['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 20
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_0,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_1 = results['randomness'][1]
    sense_list = cui_1['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 8
    isas_list = cui_1['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 17
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_1,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_2 = results['randomness'][2]
    sense_list = cui_2['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 5
    isas_list = cui_2['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 5
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_2,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_3 = results['randomness'][3]
    sense_list = cui_3['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 10
    isas_list = cui_3['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 20
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_3,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_4 = results['randomness'][4]
    sense_list = cui_4['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 11
    isas_list = cui_4['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 19
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_4,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_5 = results['randomness'][5]
    sense_list = cui_5['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 14
    isas_list = cui_5['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 20
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_5,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_6 = results['randomness'][6]
    sense_list = cui_6['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 30
    isas_list = cui_6['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 19
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_6,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_7 = results['randomness'][7]
    sense_list = cui_7['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 3
    isas_list = cui_7['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 2
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_7,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_8 = results['randomness'][8]
    sense_list = cui_8['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 6
    isas_list = cui_8['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 11
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_8,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_9 = results['randomness'][9]
    sense_list = cui_9['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 3
    isas_list = cui_9['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 1
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_9,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_10 = results['randomness'][10]
    sense_list = cui_10['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 5
    isas_list = cui_10['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 20
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_10,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_11 = results['randomness'][11]
    sense_list = cui_11['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 11
    isas_list = cui_11['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 19
    # note that there is one label w/o number
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_11,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_12 = results['randomness'][12]
    sense_list = cui_12['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 4
    isas_list = cui_12['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 9
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_12,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_13 = results['randomness'][13]
    sense_list = cui_13['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 3
    isas_list = cui_13['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 0
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_13,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_14 = results['randomness'][14]
    sense_list = cui_14['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 5
    isas_list = cui_14['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 19
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_14,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_15 = results['randomness'][15]
    sense_list = cui_15['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 3
    isas_list = cui_15['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 7
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_15,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_16 = results['randomness'][16]
    sense_list = cui_16['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 1
    isas_list = cui_16['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 3
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_16,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_17 = results['randomness'][17]
    sense_list = cui_17['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 4
    isas_list = cui_17['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 17
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_17,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_18 = results['randomness'][18]
    sense_list = cui_18['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 4
    isas_list = cui_18['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 4
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_18,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    # search for 'Camp Morton#MWE' in JoBimText
    # -- http://ltmaggie.informatik.uni-hamburg.de/jobimviz/#  and manually count
    cui_0 = results['Camp Morton'][0]
    sense_list = cui_0['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 13
    isas_list = cui_0['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 2
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_0,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_1 = results['Camp Morton'][1]
    sense_list = cui_1['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 17
    isas_list = cui_1['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 19
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_1,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_2 = results['Camp Morton'][2]
    sense_list = cui_2['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 3
    isas_list = cui_2['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 0
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_2,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_3 = results['Camp Morton'][3]
    sense_list = cui_3['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 7
    isas_list = cui_3['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 20
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_3,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_4 = results['Camp Morton'][4]
    sense_list = cui_4['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 4
    isas_list = cui_4['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 16
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_4,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    # search for 'Los Angeles#MWE' in JoBimText
    # -- http://ltmaggie.informatik.uni-hamburg.de/jobimviz/#  and manually count
    cui_0 = results['Los Angeles'][0]
    sense_list = cui_0['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 62
    isas_list = cui_0['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 16
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_0,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_1 = results['Los Angeles'][1]
    sense_list = cui_1['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 41
    isas_list = cui_1['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 18
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_1,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_2 = results['Los Angeles'][2]
    sense_list = cui_2['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 6
    isas_list = cui_2['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 15
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_2,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_3 = results['Los Angeles'][3]
    sense_list = cui_3['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 2
    isas_list = cui_3['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 1
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_3,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_4 = results['Los Angeles'][4]
    sense_list = cui_4['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 12
    isas_list = cui_4['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 19
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_4,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_5 = results['Los Angeles'][5]
    sense_list = cui_5['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 5
    isas_list = cui_5['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 18
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_5,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_6 = results['Los Angeles'][6]
    sense_list = cui_6['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 3
    isas_list = cui_6['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 18
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_6,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_7 = results['Los Angeles'][7]
    sense_list = cui_7['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 9
    isas_list = cui_7['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 16
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_7,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_8 = results['Los Angeles'][8]
    sense_list = cui_8['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 3
    isas_list = cui_8['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 17
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_8,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_9 = results['Los Angeles'][9]
    sense_list = cui_9['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 3
    isas_list = cui_9['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 18
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_9,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_10 = results['Los Angeles'][10]
    sense_list = cui_10['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 10
    isas_list = cui_10['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 18
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_10,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_11 = results['Los Angeles'][11]
    sense_list = cui_11['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 3
    isas_list = cui_11['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 17
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_11,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_12 = results['Los Angeles'][12]
    sense_list = cui_12['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 8
    isas_list = cui_12['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 5
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_12,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_13 = results['Los Angeles'][13]
    sense_list = cui_13['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 10
    isas_list = cui_13['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 16
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_13,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_14 = results['Los Angeles'][14]
    sense_list = cui_14['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 2
    isas_list = cui_14['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 7
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_14,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_15 = results['Los Angeles'][15]
    sense_list = cui_15['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 1
    isas_list = cui_15['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 18
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_15,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_16 = results['Los Angeles'][16]
    sense_list = cui_16['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 2
    isas_list = cui_16['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 4
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_16,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    cui_17 = results['Los Angeles'][17]
    sense_list = cui_17['senses']
    assert len([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]) == 3
    isas_list = cui_17['isas']
    assert len([isas.split(':')[0] for isas in isas_list]) == 0
    processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=cui_17,
                                                                                  number_of_cluster_terms=None,
                                                                                  number_of_isas=None,
                                                                                  apply_postprocess=False,
                                                                                  nlp=None, inflect_engine=None,
                                                                                  noisy_isas=[])
    assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not sense.startswith('^')]))
    assert len(processed_isas) == len(set([isas.split(':')[0] for isas in isas_list]))

    # test-2: w/o postprocessing -- "noisy_isas" with different types of isas
    # randomly 200 mentions are taken and checked random 1 sense of each
    # https://docs.python.org/3/library/random.html
    # In the future, the population must be a sequence. Instances of set are no longer supported...
    mentions_with_results = [mention for mention in results if len(results[mention]) > 1]

    samples = random.sample(population=mentions_with_results, k=200)
    count = 0
    for mention in samples:
        # https://docs.python.org/3/library/random.html#random.randint
        # a <= N <= b
        sample_cui_id = random.randint(0, len(results[mention])-1)
        sample_cui = results[mention][sample_cui_id]
        sense_list = sample_cui['senses']
        isas_list = sample_cui['isas']
        if len(isas_list) > 0:
            count += 1
        processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=sample_cui,
                                                                                      number_of_cluster_terms=None,
                                                                                      number_of_isas=None,
                                                                                      apply_postprocess=False,
                                                                                      nlp=None, inflect_engine=None,
                                                                                      noisy_isas=['thing', 'person',
                                                                                                  'location',
                                                                                                  'object',
                                                                                                  'organization',
                                                                                                  'place', 'entity',
                                                                                                  'time', 'event'])
        # noisy_isas = general types from ufet + 'thing'
        assert len(processed_senses) == len(set([sense.split('#')[0] for sense in sense_list if not
                                                 sense.startswith('^')]))
        noisy_isas = ['thing', 'person', 'location', 'object', 'organization', 'place', 'entity', 'time', 'event']
        isas_set = set([isas.split(':')[0] for isas in isas_list])
        remove = [isas for isas in noisy_isas if isas in isas_set]
        assert len(processed_isas) == len(isas_set) - len(remove)
    assert count > 100

    # test-3: w/o postprocessing, number of limitations for sense terms and isas
    mentions_with_results = [mention for mention in results if len(results[mention]) > 1]
    # print(len(mentions_with_results))

    samples = random.sample(population=mentions_with_results, k=200)
    for mention in samples:
        sample_cui_id = random.randint(0, len(results[mention])-1)
        sample_cui = results[mention][sample_cui_id]
        processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=sample_cui,
                                                                                      number_of_cluster_terms=20,
                                                                                      number_of_isas=20,
                                                                                      apply_postprocess=False,
                                                                                      nlp=None, inflect_engine=None,
                                                                                      noisy_isas=[])
        assert len(processed_senses) <= 20
        assert len(processed_senses) <= 20
        processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=sample_cui,
                                                                                      number_of_cluster_terms=10,
                                                                                      number_of_isas=10,
                                                                                      apply_postprocess=False,
                                                                                      nlp=None, inflect_engine=None,
                                                                                      noisy_isas=[])
        assert len(processed_senses) <= 10
        assert len(processed_senses) <= 10
        processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=sample_cui,
                                                                                      number_of_cluster_terms=5,
                                                                                      number_of_isas=5,
                                                                                      apply_postprocess=False,
                                                                                      nlp=None, inflect_engine=None,
                                                                                      noisy_isas=[])
        assert len(processed_senses) <= 5
        assert len(processed_senses) <= 5

    # test-4: with postprocess -- sample mentions and check the results,
    # 1- all lowerized, 2- underscore in multi-token isas should be,
    # could not check returned isas list should be in original isas list since "person people"
    # 3- with types all isas should be in w/o types and in types vocab

    # check for all types of outputs -- coming from different inputs
    import preprocess

    nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')
    nlp_headwords = stanza.Pipeline(lang='en', processors='tokenize,pos,lemma,depparse')
    inflect_engine = inflect.engine()
    with open("../open_type/release/ontology/types.txt", 'r') as f:
        types_lines = f.readlines()
    types = [type_.strip() for type_ in types_lines]

    processed_mentions_nltk_n1_first_singularized = preprocess.get_first_ngram_of_mentions(mentions=mentions, n=1,
                                                                                           inflect_engine=inflect_engine,
                                                                                           nlp=nlp,
                                                                                           apply_preprocess=True)
    processed_mentions_nltk_n1_first_results = {mention: jobimtext_handler.get_senses_from_jobimtext(
        mention=processed_mentions_nltk_n1_first_singularized[mention], cluster_type='200,200') for mention in mentions}

    #############################

    processed_mentions_nltk_n1_last_singularized = preprocess.get_last_ngram_of_mentions(mentions=mentions, n=1,
                                                                                         inflect_engine=inflect_engine,
                                                                                         nlp=nlp, apply_preprocess=True)
    processed_mentions_nltk_n1_last_results = {mention: jobimtext_handler.get_senses_from_jobimtext(
        mention=processed_mentions_nltk_n1_last_singularized[mention], cluster_type='200,200') for mention in mentions}
    #############################
    processed_mentions_headword_singularized, _ = preprocess.get_headword_of_mentions(mentions=mentions,
                                                                                      inflect_engine=inflect_engine,
                                                                                      nlp=nlp_headwords,
                                                                                      apply_preprocess=True)
    processed_mentions_headword_results = {mention: jobimtext_handler.get_senses_from_jobimtext(
        mention=processed_mentions_headword_singularized[mention], cluster_type='200,200') for mention in mentions}

    # https://docs.python.org/3/library/random.html
    # In the future, the population must be a sequence. Instances of set are no longer supported...
    mention_sample_200 = random.sample(population=list(mentions), k=200)
    for mention in mention_sample_200:
        result_headword = processed_mentions_headword_results[mention]
        if result_headword:
            if len(result_headword) == 1:
                cui_headword = result_headword[0]
            else:
                # select random one sense and check
                # a <= n <= b, https://docs.python.org/3/library/random.html#random.randint
                cui_headword = result_headword[random.randint(0, len(result_headword)-1)]
            original_headword_isas = [isas.split(':')[0] for isas in cui_headword['isas']]
            processed_headword_senses, processed_headword_isas = jobimtext_handler.process_jobimtext_result(
                result=cui_headword, number_of_cluster_terms=None, number_of_isas=None, apply_postprocess=True,
                nlp=nlp, inflect_engine=inflect_engine, noisy_isas=[])

            assert len(set(processed_headword_isas)) == len(processed_headword_isas)
            for index, label in enumerate(processed_headword_isas):
                assert label == label.lower()
                if '_' in label:
                    multi_token = [l for l in original_headword_isas if len(l.split()) > 1]
                    assert len(multi_token) > 0

            pro_headword_senses_types, pro_headword_isas_types = jobimtext_handler.process_jobimtext_result(
                result=cui_headword, number_of_cluster_terms=None, number_of_isas=None, apply_postprocess=True,
                types=types, nlp=nlp, inflect_engine=inflect_engine, noisy_isas=[])

            for label in pro_headword_isas_types:
                assert label in processed_headword_isas
                assert label in types

        result_first = processed_mentions_nltk_n1_first_results[mention]
        if result_first:
            if len(result_first) == 1:
                cui_first = result_first[0]
            else:
                cui_first = result_first[random.randint(0, len(result_first)-1)]
            original_first_isas = [isas.split(':')[0] for isas in cui_first['isas']]
            processed_first_senses, processed_first_isas = jobimtext_handler.process_jobimtext_result(
                result=cui_first, number_of_cluster_terms=None, number_of_isas=None, apply_postprocess=True,
                nlp=nlp, inflect_engine=inflect_engine, noisy_isas=[])

            assert len(set(processed_first_isas)) == len(processed_first_isas)
            for index, label in enumerate(processed_first_isas):
                assert label == label.lower()
                if '_' in label:
                    multi_token = [l for l in original_first_isas if len(l.split()) > 1]
                    assert len(multi_token) > 0
            pro_first_senses_types, pro_first_isas_types = jobimtext_handler.process_jobimtext_result(
                result=cui_first, number_of_cluster_terms=None, number_of_isas=None, apply_postprocess=True,
                types=types, nlp=nlp, inflect_engine=inflect_engine, noisy_isas=[])

            for label in pro_first_isas_types:
                assert label in processed_first_isas
                assert label in types

        result_last = processed_mentions_nltk_n1_last_results[mention]
        if result_last:
            if len(result_last) == 1:
                cui_last = result_last[0]
            else:
                cui_last = result_last[random.randint(0, len(result_last)-1)]
            original_last_isas = [isas.split(':')[0] for isas in cui_last['isas']]
            processed_last_senses, processed_last_isas = jobimtext_handler.process_jobimtext_result(
                result=cui_last, number_of_cluster_terms=None, number_of_isas=None, apply_postprocess=True,
                nlp=nlp, inflect_engine=inflect_engine, noisy_isas=[])

            assert len(set(processed_last_isas)) == len(processed_last_isas)
            for index, label in enumerate(processed_last_isas):
                assert label == label.lower()
                if '_' in label:
                    multi_token = [l for l in original_last_isas if len(l.split()) > 1]
                    assert len(multi_token) > 0
            processed_last_senses_types, processed_last_isas_types = jobimtext_handler.process_jobimtext_result(
                result=cui_last, number_of_cluster_terms=None, number_of_isas=None, apply_postprocess=True,
                types=types, nlp=nlp, inflect_engine=inflect_engine, noisy_isas=[])

            for label in processed_last_isas_types:
                assert label in processed_last_isas
                assert label in types

    # test-5: with postprocessing, number of limitations for sense terms and isas
    mentions_with_results = [mention for mention in results if len(results[mention]) > 1]
    # print(len(mentions_with_results))

    samples = random.sample(population=mentions_with_results, k=200)
    for mention in samples:
        sample_cui_id = random.randint(0, len(results[mention])-1)
        sample_cui = results[mention][sample_cui_id]
        processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=sample_cui,
                                                                                      number_of_cluster_terms=20,
                                                                                      number_of_isas=20,
                                                                                      apply_postprocess=True,
                                                                                      nlp=nlp,
                                                                                      inflect_engine=inflect_engine,
                                                                                      types=types,
                                                                                      noisy_isas=[])
        assert len(processed_senses) <= 20
        assert len(processed_senses) <= 20
        processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=sample_cui,
                                                                                      number_of_cluster_terms=10,
                                                                                      number_of_isas=10,
                                                                                      apply_postprocess=True,
                                                                                      nlp=nlp,
                                                                                      inflect_engine=inflect_engine,
                                                                                      types=types,
                                                                                      noisy_isas=[])
        assert len(processed_senses) <= 10
        assert len(processed_senses) <= 10
        processed_senses, processed_isas = jobimtext_handler.process_jobimtext_result(result=sample_cui,
                                                                                      number_of_cluster_terms=5,
                                                                                      number_of_isas=5,
                                                                                      apply_postprocess=True,
                                                                                      nlp=nlp,
                                                                                      inflect_engine=inflect_engine,
                                                                                      types=types,
                                                                                      noisy_isas=[])
        assert len(processed_senses) <= 5
        assert len(processed_senses) <= 5


def test_postprocess():
    # test: take all isas from all different input configs,
    # sample from this isas all list singular version is returned if they do not end with 's'

    # check for all types of outputs -- coming from different inputs
    import preprocess

    nlp = stanza.Pipeline(lang='en', processors='tokenize,pos')
    nlp_headwords = stanza.Pipeline(lang='en', processors='tokenize,pos,lemma,depparse')
    inflect_engine = inflect.engine()

    f = open("../open_type/release/crowd/dev.json", "r")
    dev_data = [json.loads(sent.strip()) for sent in f.readlines()]

    mentions = set([mention_info['mention_span'] for mention_info in dev_data])

    processed_mentions_nltk_n1_first_singularized = preprocess.get_first_ngram_of_mentions(mentions=mentions, n=1,
                                                                                           inflect_engine=inflect_engine,
                                                                                           nlp=nlp,
                                                                                           apply_preprocess=True)
    processed_mentions_nltk_n1_first_results = {mention: jobimtext_handler.get_senses_from_jobimtext(
        mention=processed_mentions_nltk_n1_first_singularized[mention], cluster_type='200,200') for mention in mentions}

    #############################

    processed_mentions_nltk_n1_last_singularized = preprocess.get_last_ngram_of_mentions(mentions=mentions, n=1,
                                                                                         inflect_engine=inflect_engine,
                                                                                         nlp=nlp, apply_preprocess=True)
    processed_mentions_nltk_n1_last_results = {mention: jobimtext_handler.get_senses_from_jobimtext(
        mention=processed_mentions_nltk_n1_last_singularized[mention], cluster_type='200,200') for mention in mentions}
    #############################
    processed_mentions_headword_singularized, _ = preprocess.get_headword_of_mentions(mentions=mentions,
                                                                                      inflect_engine=inflect_engine,
                                                                                      nlp=nlp_headwords,
                                                                                      apply_preprocess=True)
    processed_mentions_headword_results = {mention: jobimtext_handler.get_senses_from_jobimtext(
        mention=processed_mentions_headword_singularized[mention], cluster_type='200,200') for mention in mentions}

    isas_list = []
    for mention in mentions:
        result_headword = processed_mentions_headword_results[mention]
        isas_list.extend([isas.split(':')[0] for cui in result_headword for isas in cui['isas']])
        result_first = processed_mentions_nltk_n1_first_results[mention]
        isas_list.extend([isas.split(':')[0] for cui in result_first for isas in cui['isas']])
        result_last = processed_mentions_nltk_n1_last_results[mention]
        isas_list.extend([isas.split(':')[0] for cui in result_last for isas in cui['isas']])
    isas_set = set(isas_list)

    # https://docs.python.org/3/library/random.html
    # In the future, the population must be a sequence. Instances of set are no longer supported...
    isas_sample_200 = random.sample(population=list(isas_set), k=200)

    for label in isas_sample_200:
        singular_label = inflect_engine.singular_noun(label)
        if singular_label:
            try:
                assert jobimtext_handler.postprocess(label=label,
                                                     inflect_engine=inflect_engine, nlp=nlp) == singular_label
            except AssertionError:
                assert label[-1].lower() == 's'
