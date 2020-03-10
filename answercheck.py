import hashlib
import numpy as np
import sympy as sym
import sys

decimal_accuracy = 5
detailedwarnings = True

# Things I fixed. Fixed Matrix rounding error
# Added more print warnings

# TODO: Fix Printwarnings
# TODO: Fix negative zeros
# TODO: Fix GIST error


def printwarning(message):
    if detailedwarnings:
        print(message)


class checkanswer():

    def __init__(self, var, hashtag=None):
        checkanswer.basic(var, hashtag)

    def basic(var, hashtag=None):
        """Fuanction that encodes answers in a string called a Hash.
        This is a one way function so a correct answer will generate the
        correct has. An incorrect answer will generate an incorrect hash."""

        print(f"Testing {var}\n")
        #curr_printopts = np.get_printoptions()
        # np.set_printoptions(threshold=sys.maxsize)
        varstr = f"{var}"
        # np.set_printoptions(threshold=curr_printopts['threshold'])

        t2 = varstr.encode("utf-8")
        m = hashlib.md5(t2)
        checktag = m.hexdigest()
        if hashtag:
            if checktag == hashtag:
                print("Answer seems to be correct")
            else:
                print("Answer seems to be incorrect")
                assert checktag == hashtag, f"Answer is incorrect {checktag}"
        else:
            raise(TypeError(f"No answer hastag provided: {checktag}"))

    def vector(A, hashtag=None):
        """Function to check matrix tipe before hashing."""
        if(type(A) is not np.matrix):
            printwarning(
                f"CheckWarning: passed variable is {type(A)} and not a numpy.matrix. Trying to convert to a array matrix using ```A = np.matrix(A)```.\n\n")
            A = np.matrix(A).astype(float)
        if not np.issubdtype(A.dtype, np.dtype(float).type):
            printwarning(
                f"CheckWarning: passed matrix is {A.dtype} and not {np.dtype(float).type}. Trying to convert to float using ```A = A.astype(float)```.\n\n")
            A = A.astype(float)
        if(A.shape[0] != 1 and A.shape[1] != 1):
            assert A.shape[0] != 1 and A.shape[
                1] != 1, f"Matrix is not of vector format {A}"
        if(A.shape[0] != 1):
            printwarning(
                f"CheckWarning: numpy.matrix is row vector. Trying to convert to a column vector using ```A = A.T```.\n\n")
            A = A.T
        vecsum = A.sum()
        if not vecsum == 1:
            printwarning(
                f"CheckWarning: Vector sum of {A} has total value of {vecsum}. Trying to normalize to unit vector to check answer using using ```A = A/{vecsum}```.\n\n")
            A = A/vecsum
        if(A[0, 0] < 0):
            printwarning(
                f"CheckWarning: First element of {A} is negative ({A[0,0]}. Trying to normalize by making this value positive using ```A = -A```.\n\n")
            A = -A
        A = np.matrix(A).astype(float)
        A = np.round(A, decimals=decimal_accuracy)
        return checkanswer.basic(A, hashtag)

    def matrix(A, hashtag=None):
        """Function to check matrix type before hashing."""
        if(type(A) is not np.matrix):
            printwarning(
                f"CheckWarning: passed variable is {type(A)} and not a numpy.matrix. Trying to convert to a array matrix using ```A = np.matrix(A)```.\n\n")
            A = np.matrix(A)
        if not np.issubdtype(A.dtype, np.dtype(float).type):
            printwarning(
                f"CheckWarning: passed matrix is {A.dtype} and not {np.dtype(float).type}. Trying to convert to float using ```A = A.astype(float)```.\n\n")
            A = A.astype(float)
        A = np.round(A, decimals=decimal_accuracy)
        if not A[A == -0].size == 0:
            printwarning(
                f"CheckWarning: Matrix contains negative values for zero.  Converting to positive values of zero using  ```A[A==-0] = 0```.\n\n")
            A[A == -0] = 0
        return checkanswer.basic(A, hashtag)

    def matrix_equivelnt(A, hashtag=None):
        """Function to convert matrix to reduced row echelon form and then run hashing."""
        if(type(A) is not np.matrix):
            printwarning(
                f"CheckWarning: passed variable is {type(A)} and not a numpy.matrix. Trying to convert to a numpy matrix using ```A = np.matrix(A).astype(float)```.\n\n")
            A = np.matrix(A).astype(float)
            A = np.round(A, decimals=decimal_accuracy)
        symA = sym.Matrix(A)
        symA = symA.rref()[0]
        A = np.matrix(symA).asfloat(float)
        return checkanswer.basic(A, hashtag)

    def float(A, hashtag=None):
        """Function to check matrix type before hashing."""
        if(type(A) is not float):
            printwarning(
                f"CheckWarning: passed variable is {type(A)} and not a float. Trying to convert to a numpy matrix using ```A = float(A)```.\n\n")
            A = float(A)
        A = np.round(A, decimals=decimal_accuracy)
        return checkanswer.basic(A, hashtag)
