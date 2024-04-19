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
#change the database name to `graphbipartite`, `graphbipartitereverseattach`, or `graphbipartitewithoutgrowth` depending on your needs
mydb = mysql.connector.connect(user='root', password='hsn123', host='localhost', database='graphbipartite')
mycursor = mydb.cursor()

def deleteAllFromDb():
    mycursor.execute("truncate subjects_data_for_visualization;")
    mycursor.execute("truncate properties_subjects_characteristics;")

def klDivergence(distribution1, distribution2):
    klDivergence = 0.0
    for key, value in distribution1.items():
        value1 = value.probability
        value2 = distribution2[key].probability

        if value1 == 0.0:
            continue

        if value2 < 1e-30:
            value2 = decimal.Decimal(1e-30)


        klDivergence += float(value1) * math.log(value1 / value2)

    return klDivergence

def dissMeasure():
    deleteAllFromDb()
    for year in ['2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015']:
        realDistribution = SortedDict()
        fictiveDistribution = SortedDict()


        all_properties = []

        query = "SELECT distinct propertyCode " \
        + "FROM properties_subjects_fictive_statistics ps, wikidata_properties wp" \
        + " where ps.property_id = wp.id and ps.year = '"+year+"'"
        mycursor.execute(query)
        result = mycursor.fetchall()
        for x in result:
            all_properties.append(x[0])

        for Property in all_properties:
            realDistribution.clear()
            fictiveDistribution.clear()
            realDistribution = SortedDict()
            fictiveDistribution = SortedDict()

            query = "SELECT id FROM `wikidata_properties` where  propertyCode = '" + str(Property) + "'";
            mycursor.execute(query)
            result = mycursor.fetchall()
            property_id = -1;
            for x in result:
                property_id = x[0]

            query = "select a.property, a.degree, a.count, cast((a.count / c.som) AS DECIMAL(12,9)) as probability, type " \
            + " FROM degree_distribution a CROSS JOIN (SELECT SUM(count) som " \
            + " FROM degree_distribution b " \
            + " where b.property = '" + str(Property) + "' and b.type = 'out' and b.year = '"+year+"') c " \
            + " where a.property = '" + str(Property) + "' and a.type = 'out' and a.year = '"+year+"' " \
            + " ORDER BY degree ASC;"
            mycursor.execute(query)
            result = mycursor.fetchall()
            for x in result:
                degree = x[1]
                value = DegreeCountAndProbability(x[2], x[3])
                realDistribution[degree] = value

            query = "SELECT b.propertyCode, a.degree, a.numberOfOccurence, cast((a.numberOfOccurence / c.som) AS DECIMAL(12,9)) as probability" \
            + " FROM wikidata_properties b , properties_subjects_fictive_statistics a " \
            + " CROSS JOIN (SELECT SUM(numberOfOccurence) som FROM properties_subjects_fictive_statistics h, wikidata_properties m" \
            + " where  m.propertyCode = '" + str(Property)+ "' and h.property_id = m.id and h.year = '"+year+"') c" \
            + " where  b.propertyCode = '" + str(Property) + "'  and a.property_id = b.id and a.year = '"+year+"'"
            mycursor.execute(query)
            result = mycursor.fetchall()
            for x in result:
                degree = x[1]
                value = DegreeCountAndProbability(x[2], x[3])
                fictiveDistribution[degree] = value


            sortedFictive = copy.deepcopy(fictiveDistribution)
            sortedReal = copy.deepcopy(realDistribution)




            for key, value in sortedReal.items():
                if not sortedFictive.__contains__(key):
                    value1 = DegreeCountAndProbability(0, 0.0)
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
                y[p] = sortedFictive[key].probability
                p += 1



            d_statistics, pvalue = ks_2samp(x, y)
            wassersteinDistance = wasserstein_distance(x, y)

            x = np.array(x)
            y = np.array(y)
            jsd = jensenshannon(x, y)

            update = "INSERT INTO properties_subjects_characteristics (property, kullback, d_statistics, wasserstein_distance, jensenshannon, year) VALUES" \
                     + "('" + str(Property) + "', '" + str(kl) + "', '" + str(d_statistics) + "', '" + str(wassersteinDistance) + "', '" + str(jsd) + "', '" + str(year) +"')"

            if update.__contains__("NaN"):
                update = update.replace("NaN","NULL")
            if update.__contains__("nan"):
                update = update.replace("nan", "NULL")
            try:
                mycursor.execute(update)
                mydb.commit()
            except:
                print('error')

            print(str(kl) + "/" + str(jsd))

            insert = "INSERT INTO subjects_data_for_visualization (property_id, degree, count, probabilityOfOccuence, type_of_data, year) VALUES "
            for key, value in sortedReal.items():
                insert += "(" + str(property_id) + ", " + str(key) + ", " + str(value.count) + ", " + str(value.probability) + " , 'real', "+str(year)+"),";
            if len(sortedReal) != 0:
                insert = insert[:-1]
                insert += ";"
                mycursor.execute(insert)
                mydb.commit()

            insert = "INSERT INTO subjects_data_for_visualization (property_id, degree, count, probabilityOfOccuence, type_of_data, year) VALUES "
            for key, value in sortedFictive.items():
                insert += "(" + str(property_id) + ", " + str(key) + ", " + str(value.count) + ", " + str(value.probability) + " , 'fictive', "+str(year)+"),"
            if len(sortedFictive) != 0:
                insert = insert[:-1]
                insert += ";"
                mycursor.execute(insert)
                mydb.commit()

if __name__ == '__main__':
    print('hello')
    dissMeasure()


