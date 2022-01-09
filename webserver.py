import cherrypy
from operator import itemgetter

allAddedTransactions = []
balances = {}
spentPointsList = []

class pointsTracker(object):

    @cherrypy.expose
    def index(self):
        return "Use a specific endpoint, not just the base url"

    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.expose
    def createTransactionAction(self):

        if cherrypy.request.method == "POST":

            currentTransaction = cherrypy.request.json
            allAddedTransactions.append(currentTransaction)
            return allAddedTransactions
        else:
            #force the request to be POST
            raise cherrypy.HTTPError(400)


    @cherrypy.tools.json_out()
    @cherrypy.tools.json_in()
    @cherrypy.expose()
    def spendPointsAction(self):

        if cherrypy.request.method == "POST":
            pointsCost = cherrypy.request.json["points"]

            #loop to create initial balances from added transactions with checks for duplicate payers
            for payerInfo in allAddedTransactions:
                if balances:
                    if payerInfo["payer"] in balances:
                        balances[payerInfo["payer"]] = balances[payerInfo["payer"]] + payerInfo["points"]
                    else:
                        balances[payerInfo["payer"]] = payerInfo["points"]
                else:
                    balances[payerInfo["payer"]] = payerInfo["points"]

            listByTimestamp = sorted(allAddedTransactions, key=itemgetter('timestamp'))

            #spend points in order of timestamp
            for payerInfoSorted in listByTimestamp:
                spentDict = {}
                payer = payerInfoSorted["payer"]
                points = payerInfoSorted["points"]

                if pointsCost == 0:
                    break
                else:
                    if pointsCost > points:
                        pointsCost = pointsCost - points
                        spentDict["payer"] = payer
                        spentDict["points"] = points

                        if len(spentPointsList) > 0:
                            for dictsInfo in spentPointsList:

                                # check for duplicate payer to combine values
                                if dictsInfo['payer'] == spentDict['payer']:
                                    dictsInfo['points'] = 0 - (dictsInfo['points'] + points)
                                    break
                                else:
                                    spentDict['points'] = 0 - points
                                    spentPointsList.append(spentDict)
                                    break
                        else:

                            spentPointsList.append(spentDict)
                    else:
                        points = 0 - pointsCost
                        pointsCost = 0
                        spentDict["payer"] = payer
                        spentDict["points"] = points
                        spentPointsList.append(spentDict)

            # Loop to update the payers balances after points have been spent
            for payers in spentPointsList:
                if payers["payer"] in balances:
                    balances[payers["payer"]] = balances[payers["payer"]] + payers["points"]
                else:
                    continue

            return spentPointsList

        else:
            raise cherrypy.HTTPError(400)


    @cherrypy.tools.json_out()
    @cherrypy.expose
    def balances(self):

        if cherrypy.request.method == "GET":

            return balances
        else:
            raise cherrypy.HTTPError(400)


cherrypy.quickstart(pointsTracker())
