# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib
import math
from matplotlib.ticker import ScalarFormatter
import powerlaw
import mysql.connector
from decimal import Decimal
import numpy as np


if __name__ == '__main__':
    subjects = "subjects"
    objects = "objects"
    sujects = "sujects"

    entityNumber = '500'

    for generalType, generalCondition, typeinout in (objects,objects,"in"),(subjects, sujects,"out"):

        precisionObjectsModel = []
        coverageObjectsModel = []
        precisionSubjectsModel = []
        coverageSubjectsModel = []

        precisionReverseAttachmentObjects = []
        coverageReverseAttachmentObjects = []
        precisionReverseAttachmentSubjects = []
        coverageReverseAttachmentSubjects = []

        precisionWithoutGrowthObjects = []
        coverageWithoutGrowthObjects = []
        precisionWithoutGrowthSubjects = []
        coverageWithoutGrowthSubjects = []

        mydb = mysql.connector.connect(user='root', password='hsn123', host='localhost', database='graphbipartite')
        mycursor = mydb.cursor()


        print("step 1")
        for year in ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022']:
            # generalType = objects
            # generalCondition = objects
            # typeinout = 'in'

            countAllQuery = "SELECT count(distinct property) " + \
                            "FROM properties_" + generalType + "_characteristics t2  " \
                            " where t2.year = '"+year+"'"
            mycursor.execute(countAllQuery)
            countAll = mycursor.fetchall()
            # ---------------------------------------------------------------------------------------------------
            countRealGreaterThan2Query =    "SELECT count(distinct t2.property)  \
                                             FROM ( \
                                                   SELECT \
                                                   property, sum(count) as " + generalCondition + "Number \
                                                   FROM \
                                                  degree_distribution \
                                                    where \
                                                    year = '"+year+"' and type = '"+typeinout+"' and property like 'P%' \
                                                    group by property \
                                            ) t1, properties_"+generalType+"_characteristics t2  \
                                            WHERE t1.property = t2.property and t2.year = '"+year+"' and t1." + generalCondition + "Number >= "+ str(entityNumber)

            mycursor.execute(countRealGreaterThan2Query)
            countRealGreaterThan2 = mycursor.fetchall()
            # ---------------------------------------------------------------------------------------------------
            countModelWorksQuery = "SELECT count(distinct t2.property)  \
                                             FROM ( \
                                                   SELECT \
                                                   property, sum(count) as " + generalCondition + "Number \
                                                   FROM \
                                                  degree_distribution \
                                                    where \
                                                    year = '"+year+"' and type = '"+typeinout+"' and property like 'P%' \
                                                    group by property \
                                            ) t1, properties_"+generalType+"_characteristics t2  \
                                            WHERE t1.property = t2.property and t2.year = '"+year+"' and t1." + generalCondition + "Number >= "+ str(entityNumber) + " and jensenshannon < 0.21"

            mycursor.execute(countModelWorksQuery)
            countModelWorks = mycursor.fetchall()
            # ---------------------------------------------------------------------------------------------------
            countModelWorksWithoutConditionsQuery = "SELECT count(distinct property) " + \
                                                    "FROM properties_" + generalType + "_characteristics t2 " + \
                                                    "WHERE t2.year = '"+year+"' and jensenshannon < 0.21"
            mycursor.execute(countModelWorksWithoutConditionsQuery)
            countModelWorksWithoutConditions = mycursor.fetchall()
            # ---------------------------------------------------------------------------------------------------

            precision = countModelWorks[0][0] / countRealGreaterThan2[0][0]
            accuracy = countModelWorksWithoutConditions[0][0] / countAll[0][0]

            precisionSubjectsModel.append(precision)
            coverageSubjectsModel.append(accuracy)
            # ---------------------------------------------------------------------------------------------------
            # ---------------------------------------------------------------------------------------------------
            # ---------------------------------------------------------------------------------------------------

            # generalType = objects
            # generalCondition = objects
            # typeinout = 'in'

            countAllQuery = "SELECT count(distinct property) " + \
                            "FROM properties_" + generalType + "_characteristics t2 "\
                            " where t2.year = '"+year+"'"
            mycursor.execute(countAllQuery)
            countAll = mycursor.fetchall()
            # ---------------------------------------------------------------------------------------------------
            countRealGreaterThan2Query =    "SELECT count(distinct t2.property)  \
                                             FROM ( \
                                                   SELECT \
                                                   property, sum(count) as " + generalCondition + "Number \
                                                   FROM \
                                                  degree_distribution \
                                                    where \
                                                    year = '"+year+"' and type = '"+typeinout+"' and property like 'P%' \
                                                    group by property \
                                            ) t1, properties_"+generalType+"_characteristics t2  \
                                            WHERE t1.property = t2.property and t2.year = '"+year+"' and t1." + generalCondition + "Number >= "+ str(entityNumber)
            mycursor.execute(countRealGreaterThan2Query)
            countRealGreaterThan2 = mycursor.fetchall()
            # ---------------------------------------------------------------------------------------------------
            countModelWorksQuery = "SELECT count(distinct t2.property)  \
                                             FROM ( \
                                                   SELECT \
                                                   property, sum(count) as " + generalCondition + "Number \
                                                   FROM \
                                                  degree_distribution \
                                                    where \
                                                    year = '"+year+"' and type = '"+typeinout+"' and property like 'P%' \
                                                    group by property \
                                            ) t1, properties_"+generalType+"_characteristics t2  \
                                            WHERE t1.property = t2.property and t2.year = '"+year+"' and t1." + generalCondition + "Number >= "+ str(entityNumber) + " and jensenshannon < 0.21"
            mycursor.execute(countModelWorksQuery)
            countModelWorks = mycursor.fetchall()
            # ---------------------------------------------------------------------------------------------------
            countModelWorksWithoutConditionsQuery = "SELECT count(distinct property) " + \
                                                    "FROM properties_" + generalType + "_characteristics t2 " + \
                                                    "WHERE t2.year = '"+year+"' and jensenshannon < 0.21"
            mycursor.execute(countModelWorksWithoutConditionsQuery)
            countModelWorksWithoutConditions = mycursor.fetchall()
            # ---------------------------------------------------------------------------------------------------

            precision = countModelWorks[0][0] / countRealGreaterThan2[0][0]
            accuracy = countModelWorksWithoutConditions[0][0] / countAll[0][0]

            precisionObjectsModel.append(precision)
            coverageObjectsModel.append(accuracy)
            # ---------------------------------------------------------------------------------------------------
            # ---------------------------------------------------------------------------------------------------
            # ---------------------------------------------------------------------------------------------------
            # ---------------------------------------------------------------------------------------------------

        mydb = mysql.connector.connect(user='root', password='hsn123', host='localhost', database='graphbipartitereverseattach')
        mycursor = mydb.cursor()
        print("step 2")
        for year in ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022']:
            # generalType = objects
            # generalCondition = objects
            # typeinout = 'in'

            countAllQuery = "SELECT count(distinct property) " + \
                            "FROM properties_" + generalType + "_characteristics t2 "\
                            " where t2.year = '"+year+"'"
            mycursor.execute(countAllQuery)
            countAll = mycursor.fetchall()
            # ---------------------------------------------------------------------------------------------------
            countRealGreaterThan2Query =    "SELECT count(distinct t2.property)  \
                                             FROM ( \
                                                   SELECT \
                                                   property, sum(count) as " + generalCondition + "Number \
                                                   FROM \
                                                  degree_distribution \
                                                    where \
                                                    year = '"+year+"' and type = '"+typeinout+"' and property like 'P%' \
                                                    group by property \
                                            ) t1, properties_"+generalType+"_characteristics t2  \
                                            WHERE t1.property = t2.property and t2.year = '"+year+"' and t1." + generalCondition + "Number >= "+ str(entityNumber)
            mycursor.execute(countRealGreaterThan2Query)
            countRealGreaterThan2 = mycursor.fetchall()
            # ---------------------------------------------------------------------------------------------------
            countModelWorksQuery = "SELECT count(distinct t2.property)  \
                                             FROM ( \
                                                   SELECT \
                                                   property, sum(count) as " + generalCondition + "Number \
                                                   FROM \
                                                  degree_distribution \
                                                    where \
                                                    year = '"+year+"' and type = '"+typeinout+"' and property like 'P%' \
                                                    group by property \
                                            ) t1, properties_"+generalType+"_characteristics t2  \
                                            WHERE t1.property = t2.property and t2.year = '"+year+"' and t1." + generalCondition + "Number >= "+ str(entityNumber) + " and jensenshannon < 0.21"
            mycursor.execute(countModelWorksQuery)
            countModelWorks = mycursor.fetchall()
            # ---------------------------------------------------------------------------------------------------
            countModelWorksWithoutConditionsQuery = "SELECT count(distinct property) " + \
                                                    "FROM properties_" + generalType + "_characteristics t2 " + \
                                                    "WHERE t2.year = '"+year+"' and jensenshannon < 0.21"
            mycursor.execute(countModelWorksWithoutConditionsQuery)
            countModelWorksWithoutConditions = mycursor.fetchall()
            # ---------------------------------------------------------------------------------------------------

            precision = countModelWorks[0][0] / countRealGreaterThan2[0][0]
            accuracy = countModelWorksWithoutConditions[0][0] / countAll[0][0]

            precisionReverseAttachmentSubjects.append(precision)
            coverageReverseAttachmentSubjects.append(accuracy)
            # ---------------------------------------------------------------------------------------------------
            # ---------------------------------------------------------------------------------------------------

            # generalType = objects
            # generalCondition = objects
            # typeinout = 'in'

            countAllQuery = "SELECT count(distinct property) " + \
                            "FROM properties_" + generalType + "_characteristics t2 "\
                            " where t2.year = '" + year + "'"
            mycursor.execute(countAllQuery)
            countAll = mycursor.fetchall()
            # ---------------------------------------------------------------------------------------------------
            countRealGreaterThan2Query =    "SELECT count(distinct t2.property)  \
                                             FROM ( \
                                                   SELECT \
                                                   property, sum(count) as " + generalCondition + "Number \
                                                   FROM \
                                                  degree_distribution \
                                                    where \
                                                    year = '"+year+"' and type = '"+typeinout+"' and property like 'P%' \
                                                    group by property \
                                            ) t1, properties_"+generalType+"_characteristics t2  \
                                            WHERE t1.property = t2.property and t2.year = '"+year+"' and t1." + generalCondition + "Number >= "+ str(entityNumber)
            mycursor.execute(countRealGreaterThan2Query)
            countRealGreaterThan2 = mycursor.fetchall()
            # ---------------------------------------------------------------------------------------------------
            countModelWorksQuery = "SELECT count(distinct t2.property)  \
                                             FROM ( \
                                                   SELECT \
                                                   property, sum(count) as " + generalCondition + "Number \
                                                   FROM \
                                                  degree_distribution \
                                                    where \
                                                    year = '"+year+"' and type = '"+typeinout+"' and property like 'P%' \
                                                    group by property \
                                            ) t1, properties_"+generalType+"_characteristics t2  \
                                            WHERE t1.property = t2.property and t2.year = '"+year+"' and t1." + generalCondition + "Number >= "+ str(entityNumber) + " and jensenshannon < 0.21"
            mycursor.execute(countModelWorksQuery)
            countModelWorks = mycursor.fetchall()
            # ---------------------------------------------------------------------------------------------------
            countModelWorksWithoutConditionsQuery = "SELECT count(distinct property) " + \
                                                    "FROM properties_" + generalType + "_characteristics t2 " + \
                                                    "WHERE  t2.year = '"+year+"' and jensenshannon < 0.21"
            mycursor.execute(countModelWorksWithoutConditionsQuery)
            countModelWorksWithoutConditions = mycursor.fetchall()
            # ---------------------------------------------------------------------------------------------------

            precision = countModelWorks[0][0] / countRealGreaterThan2[0][0]
            accuracy = countModelWorksWithoutConditions[0][0] / countAll[0][0]

            precisionReverseAttachmentObjects.append(precision)
            coverageReverseAttachmentObjects.append(accuracy)

            # ---------------------------------------------------------------------------------------------------
            # ---------------------------------------------------------------------------------------------------
            # ---------------------------------------------------------------------------------------------------
            # ---------------------------------------------------------------------------------------------------

        mydb = mysql.connector.connect(user='root', password='hsn123', host='localhost', database='graphbipartitewithoutgrowth')
        mycursor = mydb.cursor()
        print("step 3")
        for year in ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022']:
            # generalType = objects
            # generalCondition = objects
            # typeinout = 'in'

            countAllQuery = "SELECT count(distinct property) " + \
                            "FROM properties_" + generalType + "_characteristics t2 "\
                            " where t2.year = '"+year+"'"
            mycursor.execute(countAllQuery)
            countAll = mycursor.fetchall()
            # ---------------------------------------------------------------------------------------------------
            countRealGreaterThan2Query =    "SELECT count(distinct t2.property)  \
                                             FROM ( \
                                                   SELECT \
                                                   property, sum(count) as " + generalCondition + "Number \
                                                   FROM \
                                                  degree_distribution \
                                                    where \
                                                    year = '"+year+"' and type = '"+typeinout+"' and property like 'P%' \
                                                    group by property \
                                            ) t1, properties_"+generalType+"_characteristics t2  \
                                            WHERE t1.property = t2.property and t2.year = '"+year+"' and t1." + generalCondition + "Number >= "+ str(entityNumber)
            mycursor.execute(countRealGreaterThan2Query)
            countRealGreaterThan2 = mycursor.fetchall()
            # ---------------------------------------------------------------------------------------------------
            countModelWorksQuery = "SELECT count(distinct t2.property)  \
                                             FROM ( \
                                                   SELECT \
                                                   property, sum(count) as " + generalCondition + "Number \
                                                   FROM \
                                                  degree_distribution \
                                                    where \
                                                    year = '"+year+"' and type = '"+typeinout+"' and property like 'P%' \
                                                    group by property \
                                            ) t1, properties_"+generalType+"_characteristics t2  \
                                            WHERE t1.property = t2.property and t2.year = '"+year+"' and t1." + generalCondition + "Number >= "+ str(entityNumber) + " and jensenshannon < 0.21"
            mycursor.execute(countModelWorksQuery)
            countModelWorks = mycursor.fetchall()
            # ---------------------------------------------------------------------------------------------------
            countModelWorksWithoutConditionsQuery = "SELECT count(distinct property) " + \
                                                    "FROM properties_" + generalType + "_characteristics t2 " + \
                                                    "WHERE t2.year = '"+year+"' and jensenshannon < 0.21"
            mycursor.execute(countModelWorksWithoutConditionsQuery)
            countModelWorksWithoutConditions = mycursor.fetchall()
            # ---------------------------------------------------------------------------------------------------

            precision = countModelWorks[0][0] / countRealGreaterThan2[0][0]
            accuracy = countModelWorksWithoutConditions[0][0] / countAll[0][0]

            precisionWithoutGrowthSubjects.append(precision)
            coverageWithoutGrowthSubjects.append(accuracy)
            # ---------------------------------------------------------------------------------------------------
            # ---------------------------------------------------------------------------------------------------

            # generalType = objects
            # generalCondition = objects
            # typeinout = 'in'

            countAllQuery = "SELECT count(distinct property) " + \
                            "FROM properties_" + generalType + "_characteristics t2 "\
                            " where t2.year = '" + year + "'"
            mycursor.execute(countAllQuery)
            countAll = mycursor.fetchall()
            # ---------------------------------------------------------------------------------------------------
            countRealGreaterThan2Query =    "SELECT count(distinct t2.property)  \
                                             FROM ( \
                                                   SELECT \
                                                   property, sum(count) as " + generalCondition + "Number \
                                                   FROM \
                                                  degree_distribution \
                                                    where \
                                                    year = '"+year+"' and type = '"+typeinout+"' and property like 'P%' \
                                                    group by property \
                                            ) t1, properties_"+generalType+"_characteristics t2  \
                                            WHERE t1.property = t2.property and t2.year = '"+year+"' and t1." + generalCondition + "Number >= "+ str(entityNumber)
            mycursor.execute(countRealGreaterThan2Query)
            countRealGreaterThan2 = mycursor.fetchall()
            # ---------------------------------------------------------------------------------------------------
            countModelWorksQuery = "SELECT count(distinct t2.property)  \
                                             FROM ( \
                                                   SELECT \
                                                   property, sum(count) as " + generalCondition + "Number \
                                                   FROM \
                                                  degree_distribution \
                                                    where \
                                                    year = '"+year+"' and type = '"+typeinout+"' and property like 'P%' \
                                                    group by property \
                                            ) t1, properties_"+generalType+"_characteristics t2  \
                                            WHERE t1.property = t2.property and t2.year = '"+year+"' and t1." + generalCondition + "Number >= "+ str(entityNumber) + " and jensenshannon < 0.21"
            mycursor.execute(countModelWorksQuery)
            countModelWorks = mycursor.fetchall()
            # ---------------------------------------------------------------------------------------------------
            countModelWorksWithoutConditionsQuery = "SELECT count(distinct property) " + \
                                                    "FROM properties_" + generalType + "_characteristics t2 " + \
                                                    "WHERE  t2.year = '"+year+"' and jensenshannon < 0.21"
            mycursor.execute(countModelWorksWithoutConditionsQuery)
            countModelWorksWithoutConditions = mycursor.fetchall()
            # ---------------------------------------------------------------------------------------------------

            precision = countModelWorks[0][0] / countRealGreaterThan2[0][0]
            accuracy = countModelWorksWithoutConditions[0][0] / countAll[0][0]

            precisionWithoutGrowthObjects.append(precision)
            coverageWithoutGrowthObjects.append(accuracy)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.set_title(""+generalType)
        years = ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022']



        ax.plot(years, precisionSubjectsModel, label=f'KRELM Precision for '+generalType, color='green')
        ax.plot(years, coverageSubjectsModel, label=f'KRELM Coverage for '+generalType, color='purple')
        ax.plot(years, precisionReverseAttachmentSubjects, label=f'Reverse Attachment Precision for '+generalType, color='green', linestyle='dashed')
        ax.plot(years, coverageReverseAttachmentSubjects, label=f'Reverse Attachment Coverage for '+generalType, color='purple', linestyle='dashed')

        ax.plot(years, precisionWithoutGrowthSubjects, label=f'Without growth Precision for '+generalType, color='green', linestyle='dotted')
        ax.plot(years, coverageWithoutGrowthSubjects, label=f'Without growth Coverage for '+generalType, color='purple', linestyle='dotted')


        legend = ax.legend()
        legend.legendHandles[0].set_markersize(3)
        ax.legend(loc='lower right', fontsize=10)


        ax.set_xlabel('Wikidata snapshot')
        ax.set_ylabel('precision and coverage')
        ax.grid(True)
        ax.set_ylim(0, 1)
        plt.savefig('curvesExp\\' + 'PrecisionAndCoverageOverYears'+generalType + '.pdf', dpi=300)
        plt.close()

    #---------------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------------
    #---------------------------------------------------------------------------------------------------------------

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4), sharey=True)

    mydb = mysql.connector.connect(user='root', password='hsn123', host='localhost', database='graphbipartite')
    mycursor = mydb.cursor()

    Property = "P161"
    typeinout = 'out'
    year = '2022'
    typeobjectssubjects = 'subjects'

    real = "select a.degree, a.count, cast((a.count / c.som) AS DECIMAL(12,9)) as probability, type " \
           + " FROM degree_distribution a CROSS JOIN (SELECT SUM(count) som " \
           + " FROM degree_distribution b " \
           + " where b.property = '" + str(
        Property) + "' and b.type = '" + typeinout + "' and b.year = '" + year + "') c " \
           + " where a.property = '" + str(
        Property) + "' and a.type = '" + typeinout + "' and a.year = '" + year + "' " \
           + " ORDER BY degree ASC;"

    model = "SELECT degree, count, probabilityOfOccuence FROM " + typeobjectssubjects + "_data_for_visualization t2, wikidata_properties t3" \
            + " where t3.id = t2.property_id and t3.propertyCode='" + Property + "' and t2.type_of_data='fictive' and t2.year = '" + year + "';"

    baseline1 = "SELECT degree, count, probabilityOfOccuence FROM " + typeobjectssubjects + "_data_for_visualization t2, wikidata_properties t3" \
                + " where t3.id = t2.property_id and t3.propertyCode='" + Property + "' and t2.type_of_data='fictive' and t2.year = '" + year + "';"

    baseline2 = "SELECT degree, count, probabilityOfOccuence FROM " + typeobjectssubjects + "_data_for_visualization t2, wikidata_properties t3" \
                + " where t3.id = t2.property_id and t3.propertyCode='" + Property + "' and t2.type_of_data='fictive' and t2.year = '" + year + "';"

    mycursor.execute(real)
    data0 = mycursor.fetchall()

    mycursor.execute(model)
    data1 = mycursor.fetchall()

    mydb = mysql.connector.connect(user='root', password='hsn123', host='localhost',
                                   database='graphbipartitereverseattach')
    mycursor = mydb.cursor()

    mycursor.execute(baseline1)
    data2 = mycursor.fetchall()

    mydb = mysql.connector.connect(user='root', password='hsn123', host='localhost',
                                   database='graphbipartitewithoutgrowth')
    mycursor = mydb.cursor()

    mycursor.execute(baseline2)
    data3 = mycursor.fetchall()

    datadegreeReal = [item[0] for item in data0]
    datacountReal = [item[2] for item in data0]

    datadegreeModel = [item[0] for item in data1]
    datacountModel = [item[2] for item in data1]

    datadegreeBase1 = [item[0] for item in data2]
    datacountBase1 = [item[2] for item in data2]

    datadegreeBase2 = [item[0] for item in data3]
    datacountBase2 = [item[2] for item in data3]

    ax1.scatter(datadegreeBase2, datacountBase2, color='Blue', label="Without growth (JSD = 0.465)")
    ax1.scatter(datadegreeBase1, datacountBase1, color='Red', label="Reverse Attach. (JSD = 0.248)")
    ax1.scatter(datadegreeReal, datacountReal, color='green', label="Wikidata")
    ax1.scatter(datadegreeModel, datacountModel, color='purple', label="KRELM (JSD = 0.143)")

    ax1.set_xlabel('out-degree', fontsize=16)
    ax2.set_ylabel("Probability Mass Function (PMF)", fontsize=16)

    ax1.set_xscale("log")
    ax1.set_yscale("log")

    ax1.legend()
    ax1.grid(True)
    # ax1.set_title('(c) Place of birth for subjects', fontsize=14)
    ax1.set_title('(c) Cast member for subjects', fontsize=14)
    # Clear the second subplot
    # -------------------------------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------------------------
    ax2.clear()
    mydb = mysql.connector.connect(user='root', password='hsn123', host='localhost', database='graphbipartite')
    mycursor = mydb.cursor()

    Property = "P161"
    typeinout = 'in'
    year = '2022'
    typeobjectssubjects = 'objects'

    real = "select a.degree, a.count, cast((a.count / c.som) AS DECIMAL(12,9)) as probability, type " \
           + " FROM degree_distribution a CROSS JOIN (SELECT SUM(count) som " \
           + " FROM degree_distribution b " \
           + " where b.property = '" + str(
        Property) + "' and b.type = '" + typeinout + "' and b.year = '" + year + "') c " \
           + " where a.property = '" + str(
        Property) + "' and a.type = '" + typeinout + "' and a.year = '" + year + "' " \
           + " ORDER BY degree ASC;"

    model = "SELECT degree, count, probabilityOfOccuence FROM " + typeobjectssubjects + "_data_for_visualization t2, wikidata_properties t3" \
            + " where t3.id = t2.property_id and t3.propertyCode='" + Property + "' and t2.type_of_data='fictive' and t2.year = '" + year + "';"

    baseline1 = "SELECT degree, count, probabilityOfOccuence FROM " + typeobjectssubjects + "_data_for_visualization t2, wikidata_properties t3" \
                + " where t3.id = t2.property_id and t3.propertyCode='" + Property + "' and t2.type_of_data='fictive' and t2.year = '" + year + "';"

    baseline2 = "SELECT degree, count, probabilityOfOccuence FROM " + typeobjectssubjects + "_data_for_visualization t2, wikidata_properties t3" \
                + " where t3.id = t2.property_id and t3.propertyCode='" + Property + "' and t2.type_of_data='fictive' and t2.year = '" + year + "';"

    mycursor.execute(real)
    data0 = mycursor.fetchall()

    mycursor.execute(model)
    data1 = mycursor.fetchall()

    mydb = mysql.connector.connect(user='root', password='hsn123', host='localhost',
                                   database='graphbipartitereverseattach')
    mycursor = mydb.cursor()

    mycursor.execute(baseline1)
    data2 = mycursor.fetchall()

    mydb = mysql.connector.connect(user='root', password='hsn123', host='localhost',
                                   database='graphbipartitewithoutgrowth')
    mycursor = mydb.cursor()

    mycursor.execute(baseline2)
    data3 = mycursor.fetchall()

    datadegreeReal = [item[0] for item in data0]
    datacountReal = [item[2] for item in data0]

    datadegreeModel = [item[0] for item in data1]
    datacountModel = [item[2] for item in data1]

    datadegreeBase1 = [item[0] for item in data2]
    datacountBase1 = [item[2] for item in data2]

    datadegreeBase2 = [item[0] for item in data3]
    datacountBase2 = [item[2] for item in data3]

    ax2.scatter(datadegreeBase2, datacountBase2, color='blue', label="Without growth (JSD = 0.277)")
    ax2.scatter(datadegreeBase1, datacountBase1, color='red', label="Reverse Attach. (JSD = 0.278)")
    ax2.scatter(datadegreeReal, datacountReal, color='green', label="wikidata")
    ax2.scatter(datadegreeModel, datacountModel, color='purple', label="KRELM (JSD = 0.142)")

    ax2.set_xlabel('in-degree', fontsize=16)
    # ax2.set_ylabel("Probability Mass Function (PMF)", fontsize=16)

    ax2.set_xscale("log")
    ax2.set_yscale("log")

    ax2.legend()
    ax2.grid(True)
    # ax2.set_title('(d) Place of birth for objects', fontsize=14)
    ax2.set_title('(d) Cast member for objects', fontsize=14)
    # Adjust spacing between subplots
    plt.tight_layout()

    # Save the figure
    plt.savefig('curvesExp\\' + 'P161combinedFigure' + '.pdf')
    plt.close()
    # -------------------------------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4), sharey=True)

    mydb = mysql.connector.connect(user='root', password='hsn123', host='localhost', database='graphbipartite')
    mycursor = mydb.cursor()

    Property = "P19"
    typeinout = 'out'
    year = '2022'
    typeobjectssubjects = 'subjects'

    real = "select a.degree, a.count, cast((a.count / c.som) AS DECIMAL(12,9)) as probability, type " \
           + " FROM degree_distribution a CROSS JOIN (SELECT SUM(count) som " \
           + " FROM degree_distribution b " \
           + " where b.property = '" + str(
        Property) + "' and b.type = '" + typeinout + "' and b.year = '" + year + "') c " \
           + " where a.property = '" + str(
        Property) + "' and a.type = '" + typeinout + "' and a.year = '" + year + "' " \
           + " ORDER BY degree ASC;"

    model = "SELECT degree, count, probabilityOfOccuence FROM " + typeobjectssubjects + "_data_for_visualization t2, wikidata_properties t3" \
            + " where t3.id = t2.property_id and t3.propertyCode='" + Property + "' and t2.type_of_data='fictive' and t2.year = '" + year + "';"

    baseline1 = "SELECT degree, count, probabilityOfOccuence FROM " + typeobjectssubjects + "_data_for_visualization t2, wikidata_properties t3" \
                + " where t3.id = t2.property_id and t3.propertyCode='" + Property + "' and t2.type_of_data='fictive' and t2.year = '" + year + "';"

    baseline2 = "SELECT degree, count, probabilityOfOccuence FROM " + typeobjectssubjects + "_data_for_visualization t2, wikidata_properties t3" \
                + " where t3.id = t2.property_id and t3.propertyCode='" + Property + "' and t2.type_of_data='fictive' and t2.year = '" + year + "';"

    mycursor.execute(real)
    data0 = mycursor.fetchall()

    mycursor.execute(model)
    data1 = mycursor.fetchall()

    mydb = mysql.connector.connect(user='root', password='hsn123', host='localhost',
                                   database='graphbipartitereverseattach')
    mycursor = mydb.cursor()

    mycursor.execute(baseline1)
    data2 = mycursor.fetchall()

    mydb = mysql.connector.connect(user='root', password='hsn123', host='localhost',
                                   database='graphbipartitewithoutgrowth')
    mycursor = mydb.cursor()

    mycursor.execute(baseline2)
    data3 = mycursor.fetchall()

    datadegreeReal = [item[0] for item in data0]
    datacountReal = [item[2] for item in data0]

    datadegreeModel = [item[0] for item in data1]
    datacountModel = [item[2] for item in data1]

    datadegreeBase1 = [item[0] for item in data2]
    datacountBase1 = [item[2] for item in data2]

    datadegreeBase2 = [item[0] for item in data3]
    datacountBase2 = [item[2] for item in data3]

    ax1.scatter(datadegreeBase2, datacountBase2, color='Blue', label="Without growth (JSD = 0.007)")
    ax1.scatter(datadegreeBase1, datacountBase1, color='Red', label="Reverse Attach. (JSD = 0.005)")
    ax1.scatter(datadegreeReal, datacountReal, color='green', label="Wikidata")
    ax1.scatter(datadegreeModel, datacountModel, color='purple', label="KRELM (JSD = 0.006)")

    ax1.set_xlabel('out-degree', fontsize=16)
    ax2.set_ylabel("Probability Mass Function (PMF)", fontsize=16)

    ax1.set_xscale("log")
    ax1.set_yscale("log")

    ax1.legend()
    ax1.grid(True)
    ax1.set_title('(a) Place of birth for subjects', fontsize=14)
    # ax1.set_title('(c) Cast member for subjects', fontsize=14)
    # Clear the second subplot
    # -------------------------------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------------------------
    ax2.clear()
    mydb = mysql.connector.connect(user='root', password='hsn123', host='localhost', database='graphbipartite')
    mycursor = mydb.cursor()

    Property = "P19"
    typeinout = 'in'
    year = '2022'
    typeobjectssubjects = 'objects'

    real = "select a.degree, a.count, cast((a.count / c.som) AS DECIMAL(12,9)) as probability, type " \
           + " FROM degree_distribution a CROSS JOIN (SELECT SUM(count) som " \
           + " FROM degree_distribution b " \
           + " where b.property = '" + str(
        Property) + "' and b.type = '" + typeinout + "' and b.year = '" + year + "') c " \
           + " where a.property = '" + str(
        Property) + "' and a.type = '" + typeinout + "' and a.year = '" + year + "' " \
           + " ORDER BY degree ASC;"

    model = "SELECT degree, count, probabilityOfOccuence FROM " + typeobjectssubjects + "_data_for_visualization t2, wikidata_properties t3" \
            + " where t3.id = t2.property_id and t3.propertyCode='" + Property + "' and t2.type_of_data='fictive' and t2.year = '" + year + "';"

    baseline1 = "SELECT degree, count, probabilityOfOccuence FROM " + typeobjectssubjects + "_data_for_visualization t2, wikidata_properties t3" \
                + " where t3.id = t2.property_id and t3.propertyCode='" + Property + "' and t2.type_of_data='fictive' and t2.year = '" + year + "';"

    baseline2 = "SELECT degree, count, probabilityOfOccuence FROM " + typeobjectssubjects + "_data_for_visualization t2, wikidata_properties t3" \
                + " where t3.id = t2.property_id and t3.propertyCode='" + Property + "' and t2.type_of_data='fictive' and t2.year = '" + year + "';"

    mycursor.execute(real)
    data0 = mycursor.fetchall()

    mycursor.execute(model)
    data1 = mycursor.fetchall()

    mydb = mysql.connector.connect(user='root', password='hsn123', host='localhost',
                                   database='graphbipartitereverseattach')
    mycursor = mydb.cursor()

    mycursor.execute(baseline1)
    data2 = mycursor.fetchall()

    mydb = mysql.connector.connect(user='root', password='hsn123', host='localhost',
                                   database='graphbipartitewithoutgrowth')
    mycursor = mydb.cursor()

    mycursor.execute(baseline2)
    data3 = mycursor.fetchall()

    datadegreeReal = [item[0] for item in data0]
    datacountReal = [item[2] for item in data0]

    datadegreeModel = [item[0] for item in data1]
    datacountModel = [item[2] for item in data1]

    datadegreeBase1 = [item[0] for item in data2]
    datacountBase1 = [item[2] for item in data2]

    datadegreeBase2 = [item[0] for item in data3]
    datacountBase2 = [item[2] for item in data3]

    ax2.scatter(datadegreeBase2, datacountBase2, color='blue', label="Without growth (JSD = 0.424)")
    ax2.scatter(datadegreeBase1, datacountBase1, color='red', label="Reverse Attach. (JSD = 0.424)")
    ax2.scatter(datadegreeReal, datacountReal, color='green', label="wikidata")
    ax2.scatter(datadegreeModel, datacountModel, color='purple', label="KRELM (JSD = 0.060)")

    ax2.set_xlabel('in-degree', fontsize=16)
    # ax2.set_ylabel("Probability Mass Function (PMF)", fontsize=16)

    ax2.set_xscale("log")
    ax2.set_yscale("log")

    ax2.legend()
    ax2.grid(True)
    ax2.set_title('(b) Place of birth for objects', fontsize=14)
    # ax2.set_title('(d) Cast member for objects', fontsize=14)
    # Adjust spacing between subplots
    plt.tight_layout()

    # Save the figure
    plt.savefig('curvesExp\\' + 'P19combinedFigure' + '.pdf')
    plt.close()

    # ---------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------------------

    mydb = mysql.connector.connect(user='root', password='hsn123', host='localhost', database='graphbipartite')
    mycursor = mydb.cursor()

    mydbAllkg = mysql.connector.connect(user='root', password='hsn123', host='localhost', database='graphbipartiteallkgmodel')
    mycursorAllkg = mydbAllkg.cursor()
    # ------------------------------------------------------------------------------------------------------------------------------------------
    matplotlib.use("Agg")
    Property = "P19"
    Property2 = "birthPlace"
    Property1 = "4449_birthPlace"

    # mycursor.execute(
    #     "SELECT degree, count FROM degree_distribution t1 where t1.property = 'P161' and type = 'in' and year = '2022';")

    query = "select a.degree, a.count, cast((a.count / c.som) AS DECIMAL(12,9)) as probability, type " \
            + " FROM degree_distribution a CROSS JOIN (SELECT SUM(count) som " \
            + " FROM degree_distribution b " \
            + " where b.property = '" + str(Property) + "' and b.type = 'in' and b.year = '2022') c " \
            + " where a.property = '" + str(Property) + "' and a.type = 'in' and a.year = '2022' " \
            + " ORDER BY degree ASC;"

    query1 = "select a.degree, a.count, cast((a.count / c.som) AS DECIMAL(12,9)) as probability, type " \
             + " FROM degree_distribution a CROSS JOIN (SELECT SUM(count) som " \
             + " FROM degree_distribution b " \
             + " where b.kg = 'DBPEDIA' and b.property = '" + str(Property1) + "' and b.type = 'in' ) c " \
             + " where a.kg = 'DBPEDIA' and a.property = '" + str(Property1) + "' and a.type = 'in' " \
             + " ORDER BY degree ASC;"

    query2 = "select a.degree, a.count, cast((a.count / c.som) AS DECIMAL(12,9)) as probability, type " \
             + " FROM degree_distribution a CROSS JOIN (SELECT SUM(count) som " \
             + " FROM degree_distribution b " \
             + " where b.kg = 'YAGO4' and b.property = '" + str(Property2) + "' and b.type = 'in' ) c " \
             + " where a.kg = 'YAGO4' and a.property = '" + str(Property2) + "' and a.type = 'in' " \
             + " ORDER BY degree ASC;"

    query3 = "SELECT degree, count, probabilityOfOccuence FROM wikidata_properties t1, subjects_data_for_visualization t2" \
             + " where t1.propertyCode='" + Property + "' and type_of_data='fictive' and t1.id=t2.property_id;"

    mycursor.execute(query);
    data = mycursor.fetchall()

    mycursor.execute(query3);
    dataModel = mycursor.fetchall()

    mycursorAllkg.execute(query1);
    dataDbpedia = mycursorAllkg.fetchall()

    mycursorAllkg.execute(query2);
    dataYago = mycursorAllkg.fetchall()

    fig, ax = plt.subplots(figsize=(8, 5))

    datadegree = [item[0] for item in data]
    datacount = [item[1] for item in data]

    datadegreeDbpedia = [item[0] for item in dataDbpedia]
    datacountDbpedia = [item[1] for item in dataDbpedia]

    datadegreeYago = [item[0] for item in dataYago]
    datacountYago = [item[1] for item in dataYago]

    datadegreeModel = [item[0] for item in dataModel]
    datacountModel = [item[1] for item in dataModel]

    ax.scatter(datadegree, datacount, color='green', label="wikidata")
    ax.scatter(datadegreeDbpedia, datacountDbpedia, color='BLUE', label="DBpedia")
    ax.scatter(datadegreeYago, datacountYago, color='RED', label="YAGO")
    # ax.scatter(datadegreeModel, datacountModel, color='blue', label="Model")

    ax.set_xlabel('Number of persons', fontsize=16)
    ax.set_ylabel("Number of places", fontsize=16)
    ax.set_title('(a) birthplace across 3 KGs', fontsize=14)
    ax.set_xscale("log")
    ax.set_yscale("log")

    ax.legend()
    ax.grid(True)


    plt.savefig('curvesExp\\' + 'P19distributionAllKg' + '.pdf')
    plt.close()
    #------------------------------------------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------------------------------------------
    # P over time
    matplotlib.use("Agg")
    Property = "P19"

    typeinout = 'in'
    year1 = '2015'
    year2 = '2017'
    year3 = '2022'

    typeobjectssubjects = 'objects'

    query = "select a.degree, a.count, cast((a.count / c.som) AS DECIMAL(12,9)) as probability, type " \
            + " FROM degree_distribution a CROSS JOIN (SELECT SUM(count) som " \
            + " FROM degree_distribution b " \
            + " where b.property = '" + str(Property) + "' and b.type = '"+typeinout+"' and b.year = '"+year1+"') c " \
            + " where a.property = '" + str(Property) + "' and a.type = '"+typeinout+"' and a.year = '"+year1+"' " \
            + " ORDER BY degree ASC;"

    query1 = "select a.degree, a.count, cast((a.count / c.som) AS DECIMAL(12,9)) as probability, type " \
            + " FROM degree_distribution a CROSS JOIN (SELECT SUM(count) som " \
            + " FROM degree_distribution b " \
            + " where b.property = '" + str(Property) + "' and b.type = '"+typeinout+"' and b.year = '"+year2+"') c " \
            + " where a.property = '" + str(Property) + "' and a.type = '"+typeinout+"' and a.year = '"+year2+"' " \
            + " ORDER BY degree ASC;"

    query2 = "select a.degree, a.count, cast((a.count / c.som) AS DECIMAL(12,9)) as probability, type " \
            + " FROM degree_distribution a CROSS JOIN (SELECT SUM(count) som " \
            + " FROM degree_distribution b " \
            + " where b.property = '" + str(Property) + "' and b.type = '"+typeinout+"' and b.year = '"+year3+"') c " \
            + " where a.property = '" + str(Property) + "' and a.type = '"+typeinout+"' and a.year = '"+year3+"' " \
            + " ORDER BY degree ASC;"

    query3 = "SELECT degree, count, probabilityOfOccuence FROM wikidata_properties t1, "+typeobjectssubjects+"_data_for_visualization t2" \
             + " where t1.propertyCode='" + Property + "' and type_of_data='fictive' and t1.id=t2.property_id;"

    mycursor.execute(query);
    data = mycursor.fetchall()

    mycursor.execute(query1);
    data1 = mycursor.fetchall()

    mycursor.execute(query2);
    data2 = mycursor.fetchall()

    mycursor.execute(query3);
    dataModel = mycursor.fetchall()

    fig, ax = plt.subplots(figsize=(8, 5))

    datadegree = [item[0] for item in data]
    datacount = [item[1] for item in data]

    datadegree1 = [item[0] for item in data1]
    datacount1 = [item[1] for item in data1]

    datadegree2 = [item[0] for item in data2]
    datacount2 = [item[1] for item in data2]

    datadegree3 = [item[0] for item in dataModel]
    datacount3 = [item[1] for item in dataModel]


    ax.scatter(datadegree, datacount, color='blue', label=""+year1, zorder = 0)
    ax.scatter(datadegree1, datacount1, color='red', label=""+year2,zorder = 1)
    ax.scatter(datadegree2, datacount2, color='green', label=""+year3, zorder = 1)
    #ax.scatter(datadegree3, datacount3, color='purple', label="model")

    ax.set_xlabel('Number of persons', fontsize=16)
    ax.set_ylabel("Number of places", fontsize=16)

    ax.set_title('(b) birthplace in Wikidata over time', fontsize=14)
    ax.set_xscale("log")
    ax.set_yscale("log")

    ax.legend()
    ax.grid(True)

    plt.savefig('curvesExp\\' + Property+'distributionYears' + '.pdf')
    plt.close()