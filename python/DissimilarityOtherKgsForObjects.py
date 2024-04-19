import mysql.connector
from sortedcontainers import SortedDict
from array import array
import math
from scipy.stats import ks_2samp
import copy
import decimal
import numpy as np
from sklearn.kernel_ridge import KernelRidge
from scipy.stats import wasserstein_distance
import statsmodels.stats.diagnostic as smd
from scipy.interpolate import interp1d
from scipy.spatial.distance import jensenshannon

class DegreeCountAndProbability:
    def __init__(self, a, b):
        self.count = a
        self.probability = b


#change the database name to `graphbipartiteallkgmodel`, `graphbipartiteallkgreverseattachment`, or `graphbipartiteallkgwithoutgrowth` depending on your needs
mydb = mysql.connector.connect(user='root', password='hsn123', host='localhost', database='graphbipartiteallkgmodel')
mycursor = mydb.cursor()

def deleteAllFromDb():
    mycursor.execute("truncate objects_data_for_visualization;")
    mycursor.execute("truncate properties_objects_characteristics;")

def klDivergence(distribution1, distribution2):
    klDivergence = 0.0
    for key,value in distribution1.items():
        value1 = value.probability
        object2 = distribution2[key]
        value2 = object2.probability


        if value1 == 0.0:
            continue

        if value2 < 1e-30:
            value2 = decimal.Decimal(1e-30)

        klDivergence += float(value1) * math.log(decimal.Decimal(value1) / decimal.Decimal(value2))
    return klDivergence

def dissMeasure():
    deleteAllFromDb()

    realDistribution = SortedDict()
    fictiveDistribution = SortedDict()

    all_kgs = ["YAGO4", "DBPEDIA", "DBNARY"]

    for kg in all_kgs:

        # if kg == "DBPEDIA" or kg == "BNF":
        #     continue;

        all_properties = []
        query = "SELECT distinct property " \
        + "FROM properties_objects_fictive_statistics" \
        + " where kg = '"+kg+"'"

        mycursor.execute(query)
        result = mycursor.fetchall()
        for x in result:
            all_properties.append(x[0])

        for Property in all_properties:

            if '\'' in Property:
                Property = Property.replace("'", "r")

            realDistribution.clear()
            fictiveDistribution.clear()
            jsd = 0
            realDistribution = SortedDict()
            fictiveDistribution = SortedDict()

            query = "select a.property, a.degree, a.count, cast((a.count / c.som) AS DECIMAL(12,9)) as probability, type " \
            + " FROM degree_distribution a CROSS JOIN (SELECT SUM(count) som " \
            + " FROM degree_distribution b " \
            + " where b.property = '" + str(Property) + "' and b.type = 'IN' and b.kg = '"+kg+"') c " \
            + " where a.property = '" + str(Property) + "' and a.type = 'IN' and a.kg = '"+kg+"' " \
            + " ORDER BY degree ASC;"
            mycursor.execute(query)
            result = mycursor.fetchall()
            for x in result:
                degree = x[1]
                value = DegreeCountAndProbability(x[2], x[3])
                realDistribution[degree] = value

            query = "SELECT property, a.degree, a.numberOfOccurence, probabilityOfOccuence as probability" \
            + " FROM properties_objects_fictive_statistics a " \
            + " where property = '" + str(Property) + "'  and a.kg = '"+kg+"'"
            mycursor.execute(query)
            result = mycursor.fetchall()
            for x in result:
                degree = x[1]
                value = DegreeCountAndProbability(x[2], x[3])
                fictiveDistribution[degree] = value

            sortedFictive = copy.deepcopy(fictiveDistribution)
            sortedReal = copy.deepcopy(realDistribution)

            sortedFictive1 = copy.deepcopy(fictiveDistribution)
            sortedReal1 = copy.deepcopy(realDistribution)



            for key, value in sortedReal.items():
                if not sortedFictive.__contains__(key):
                    v = 0.0
                    value1 = DegreeCountAndProbability(0, v)
                    sortedFictive[key] = value1

            for key, value in sortedFictive.items():
                if not sortedReal.__contains__(key):
                    value1 = DegreeCountAndProbability(0, 0.0)
                    sortedReal[key] = value1

            kl = klDivergence(sortedReal, sortedFictive)



            x = array('d', [0.0] * len(sortedReal))
            y = array('d', [0.0] * len(sortedFictive))
            p = 0

            for key, value in sortedReal.items():
                x[p] = value.probability
                object2 = sortedFictive[key]
                y[p] = object2.probability
                p += 1

            x = np.array(x)
            y = np.array(y)
            jsd = jensenshannon(x, y)

            try:
                d_statistics, pvalue = ks_2samp(x, y)
                # Compute the Wasserstein distance between the two distributions
                wassersteinDistance = wasserstein_distance(x, y)
            except:
                d_statistics = 1
                wassersteinDistance = 1




            update = "INSERT INTO properties_objects_characteristics (property, kg, kullback, d_statistics, jensenshannon) VALUES" \
                     + "('" + str(Property) + "', '"+kg+"', '" + str(kl) + "', '" + str(d_statistics) + "', " + str(jsd) + ")"

            if update.__contains__("NaN"):
                update = update.replace("NaN", "NULL")

            if update.__contains__("nan"):
                update = update.replace("nan", "NULL")

            try:
                mycursor.execute(update)
                mydb.commit()
            except:
                print('error')

            print(str(jsd)+"/"+str(d_statistics))

            insert = "INSERT INTO objects_data_for_visualization (property, degree, count, probabilityOfOccuence, type_of_data, kg) VALUES "
            for key, value in sortedReal.items():
                insert += "('" + str(Property) + "', " + str(key) + ", " + str(value.count) + ", " + str(value.probability) + " , 'real', '"+ kg +"'),";
            if len(sortedReal1) != 0:
                insert = insert[:-1]
                insert += ";"
                mycursor.execute(insert)
                mydb.commit()

            insert = "INSERT INTO objects_data_for_visualization (property, degree, count, probabilityOfOccuence, type_of_data, kg) VALUES "
            for key, value in sortedFictive.items():
                insert += "('" + str(Property) + "', " + str(key) + ", " + str(value.count) + ", " + str(value.probability) + " , 'fictive', '"+ kg +"'),"
            if len(sortedFictive1) != 0:
                insert = insert[:-1]
                insert += ";"
                mycursor.execute(insert)
                mydb.commit()

if __name__ == '__main__':
    print('hello')
    dissMeasure()


