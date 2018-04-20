import sys

"""
Author: Ethan T. Hendrix
Date: 18.04.2018
Organization: College of Charleston
Department: Computer Science
About: This code was developed for GEOL 395 - a special topics class in which
    we use SAC to examine binary files containing seismic data. The following
    functions are used to help with the process of taking seismic binary data
    and performing Fourier Transformations to reveal a Rayleigh Dispersion
    Curve.
NOTE: All of this code is free and publicly available for anyone to use.
Documentation: http://github.com/hendrixet/sach
"""

def new_b_time():
    """
    Calculate the new B time - hard-coded for the moment
    """
    b = 1507300 # will be calculated in future
    return b

def create_macro(b1_original,b1_new,file1,b2_original,b2_new,file2,pval):
    """
    Create the macro that we can run in SAC - many values are hard-coded while
    in development. Macros in SAC are just text files - constructing this text
    file is the goal of this method
    """
    START = "bg x\ncolor on increment\nqdp off\n" # Basic start in SAC
    out = open("perform-fft","w")
    ## file1 = "R1_1.sac"
    ## file2 = "C4_1.sac"
    newfile1 = file1.split(".")[0] + str(pval) + ".sac"
    newfile2 = file2.split(".")[0] + str(pval) + ".sac"
    outfile = file1.split(".")[0] + "_" + file2.split(".")[0] + str(pval) + ".sac"

    macro = ""

    macro += START # add this to the beginning once
    macro += "read " + file1 + "\n" # read our first file in
    macro += "ch B " + str(b1_new) + "\n"
    macro += "cut " + str(b1_original) + " " + str(b1_new) + "\n"
    macro += "write over " + newfile1 + "\n"
    macro += "cut " + str(b2_original) + " " + str(b2_new) + "\n"
    macro += "read " + file2 + "\n"
    macro += "write over " + newfile2 + "\n"
    macro += "read " + newfile2 + "\n"
    macro += "addf " + newfile1 + "\n"
    macro += "write over " + outfile + "\n"
    macro += "p1\n"
    macro += "taper\n"
    macro += "fft\n"
    macro += "plotsp\n"
    macro += "writesp am " + outfile.split(".")[0] + "\n"
    macro += "read *am\n"
    macro += "loglog\n"
    macro += "p1\n"

    out.write(macro)
    out.close()

def read_file():
    """
    This is going to read our and return a two dimensional array of every
    station's information.
    """
    ## file_name = input("please enter your file from the current working directory")
    file_name = "test.txt"
    fin = open(file_name,"r")
    station_information = []
    for line in file:
        station_information.append(line.split("|"))
    return station_information

def time_diff( b1 , b2 ):
    """
    find the time difference given two b values
    if you get 0 something is wrong and you've given the same time somehow
    """
    if ( b1 > b2 ):
        return b1 - b2
    elif ( b1 < b2 ) :
        return b2 - b1
    else:
        return 0

def dist(n1,e1,n2,e2):
    """
    basic euclidian distance formula given two points on a map
    """
    return math.sqrt( (e2-e1)**2 + (n2-n1)**2 )

def find_station_distances(station_list):
    """
    find the distance between two stations given station list
    """
    output = ""
    for i in range(len(station_list)):
        station = station_list[i][0]
        n1 = station_list[i][1]
        e1 = station_list[i][2]
        for j in range(len(station_list[i:-1])):
            next_station = station_list[j][0]
            n2 = station_list[j][1]
            e2 = station_list[j][2]
            distance = dist(n1,e1,n2,e2)
            output += station + " -> " + next_station + "= " + str(distance) +" m\n"
    out = open("distances.txt","w")
    out.write(output)
    out.close()


def main():
    print("Welcome to SACH!")
    b1_new = 157300
    b1_original = 15700
    b2_new = 15700 + 1310.715
    b2_original =  15700
    pval = 0.001
    file1 = "R1_1.sac"
    file2 = "C4_1.sac"

    create_macro(b1_original, b1_new, file1, b2_original, b2_new, file2, pval)

if __name__ == "__main__":
    main()
