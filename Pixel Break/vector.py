# Adam Fahrer
# Lab_06
# 2/18/2021
# Ben Wade
import math


class Vector(object):
    def __init__(self, *values):
        """
        The constructor
        :param values: A variable length argument of ints or floats
        :return: N/A for constructors
        """
        self.p_norm = 0
        self.data = []
        for value in values:
            if isinstance(value, (int, float)):
                self.data.append(float(value))
            else:
                raise TypeError("Only integer or float values can be accepted.")
        self.dim = len(self.data)
        self.x = values[0]
        self.y = values[1]

    def norm(self, p):
        """Determining what type of p-norm it is"""
        if isinstance(p, int):
            return self.p_norm == p
        if p == "infinity":
            return abs(max(self.data))
        else:
            raise TypeError("Only integers or infinity can be accepted")

    def mag(self):
        """Returns the norm of the Vector"""
        if self.p_norm != "infinity":
            return float((((abs(self.data[0])) ** self.p_norm) + ((abs(self.data[1])) ** self.p_norm) + (
                    (abs(self.data[2])) ** self.p_norm)) ** 1 / self.p_norm)
        else:
            pass

    def mag_squared(self):
        """Returns the non-squared norm of the Vector"""
        if self.p_norm == 2:
            return float((((abs(self.data[0])) ** self.p_norm) + ((abs(self.data[1])) ** self.p_norm) + (
                (abs(self.data[2])))))
        else:
            pass

    def normalize(self):
        """Returns the Vector in the same direction"""
        return Vector(abs(self.data[0]), abs(self.data[1]), abs(self.data[2]))

    def is_zero(self):
        """Checks to see if the entire Vector is 0"""
        i = 0
        while i < self.dim:
            if self.data[i] != 0:
                return False
            else:
                i += 1
        return True

    def dot(self, v1, v2):
        """Preforming the dot product"""
        if v1.dim == v2.dim:
            i = 0
            sum = 0
            while i < v1.dim:
                d = v1[i] * v2[i]
                sum += d
                i += 1
            return sum

    def i(self):
        """Converts the Vector into a coordinate"""
        new_date = []
        for values in self.data:
            if isinstance(values, (int, float)):
                new_date.append(int(values))
        return new_date

    def __getitem__(self, index):
        """
        :param index: An integer index
        :return: The float value at position index
        """

        return self.data[index]

    def __setitem__(self, index, value):
        """
        :param index: integer index to be updated
        :param value: New Value
        :return: Returns None. Changes the list index with the value
        """
        i = self.data[index]
        self.data.remove(i)
        self.data.insert(index, value)
        return self.data[index]

    def __str__(self):
        """Converts an instance of the fraction class for printing"""
        """return: formatted string representing of the Fraction instance"""
        vector_statement = "<Vector" + str(self.dim) + ": " + str(self.data) + ">"
        return vector_statement.replace('[', "").replace(']', "")

    def __len__(self, *values):
        """Converts an instance of the fraction class for printing"""
        """return: formatted string representing of the Fraction instance"""
        counter = 0
        for i in values:
            counter += 1
        return print(counter)

    def __add__(self, other):
        """Overload the operator to add two Fractions
        and return: new Fraction with correct values"""
        if isinstance(other, Vector):
            x = self.data[0] + other.data[0]
            y = self.data[1] + other.data[1]
            z = self.data[2] + other.data[2]
            return Vector(x, y, z)
        else:
            raise TypeError("You can only add another Vector to this Vector (You passed ", other, ").")

    def __copy__(self):
        """Copying the vector"""
        new_data = self.data.copy()
        return new_data

    def __mul__(self, other):
        """Return: The product of a Fraction and either a Fraction or an integer"""
        if isinstance(other, int):
            return Vector(self.data[0] * other, self.data[1] * other, self.data[2] * other)
        else:
            raise TypeError("Can only multiply vectors with scalar")

    def __rmul__(self, other):
        """Tell python what to do when multiplying on the right hand side"""
        if isinstance(other, int):
            x = self.data[0] * other
            y = self.data[1] * other
            z = self.data[2] * other
            return Vector(x, y, z)
        else:
            raise TypeError("Can only multiply vectors with scalar")

    def __sub__(self, other):
        """Telling python to subtract when needed"""
        if isinstance(other, Vector):
            x = self.data[0] + (-1) * other.data[0]
            y = self.data[1] + (-1) * other.data[1]
            z = self.data[2] + (-1) * other.data[2]
            return Vector(x, y, z)
        else:
            raise TypeError("You can only sub another Vector to this Vector (You passed ", other, ")")

    def __rsub__(self, other):
        """Subtracting from the right side"""
        if isinstance(other, Vector):
            x = self.data[0] + other.data[0]
            return Vector(x)
        else:
            raise TypeError("You can only sub another Vector to this Vector (You passed ", other, ")")

    def __neg__(self):
        """Return: Negative of a Fraction"""
        x = self.data[0] * -1
        y = self.data[1] * -1
        z = self.data[2] * -1
        return Vector(x, y, z)

    def __eq__(self, other):
        """Checks if both fractions are equal to each other"""
        if self.data == other.data:
            return True
        else:
            return False

    def __truediv__(self, other):
        """Divides a vector by a integer or float"""
        if isinstance(other, (int, float)):
            x = self.data[0] / other
            y = self.data[1] / other
            z = self.data[2] / other
            return Vector(x, y, z)


class Vector2(Vector):
    def __init__(self, x, y):
        """
        :param x: An x and y value for the vector
        :param y: A vector instance the is both Vector and Vector2
        """
        super().__init__(x, y)

    def degree(self):
        """Finds the degree of a Vector"""
        equation = math.atan(self.data[1] / self.data[0])
        outcome = math.degrees(equation)
        return int(outcome)

    def degree_inv(self):
        """Finds the degree of a Vector of a standard coordinate system"""
        self.data[1] = self.data[1] * -1
        equation = math.atan(self.data[1] / self.data[0])
        outcome = math.degrees(equation)
        return int(outcome)

    def radians(self):
        """Finds the radians of a Vector"""
        return math.radians(self.degree())

    def radians_inv(self):
        """Finds the radians of a Vector of a standard coordinate system"""
        return math.radians(self.degree_inv())

    def perpendicular(self):
        """Makes a perpendicular Vectors from the original Vector"""
        return Vector2(-self.data[0], self.data[1])

    @property
    def x(self):
        """
        :param self: A Vector2 instance
        :return: The x component
        """
        return self[0]

    @property
    def y(self):
        """
        :param self: A Vector2 instance
        :return: The y component
        """
        return self[1]

    @x.setter
    def x(self, newvalue):
        """
        :param newvalue: A Vector2 instance and the value you want to change x to.
        :return: Changes x value to new value.
        """
        if isinstance(newvalue, (int, float)):
            self[0] = float(newvalue)
        else:
            raise TypeError("Only integer or float values can be accepted.")

    @y.setter
    def y(self, newvalue):
        """
        :param newvalue: A Vector2 instance and the value you want to change y to.
        :return: Changes y value to new value.
        """
        if isinstance(newvalue, (int, float)):
            self[1] = float(newvalue)
        else:
            raise TypeError("Only integer or float values can be accepted.")


class Vector3(Vector):
    def __init__(self, x, y, z):
        """
        :param x: An x, y, and z values for the vector
        :param y: A vector instance the is Vector, Vector2, and Vector3
        """
        super().__init__(x, y, z)

    @property
    def x(self):
        """
        :param self: A Vector3 instance
        :return: The x component
        """
        return self[0]

    @property
    def y(self):
        """
        :param self: A Vector3 instance
        :return: The y component
        """
        return self[1]

    @property
    def z(self):
        """
        :param self: A Vector3 instance
        :return: The z component
        """
        return self[3]

    @x.setter
    def x(self, newvalue):
        """
        :param newvalue: A Vector3 instance and the value you want to change x to.
        :return: Changes x value to new value.
        """
        if isinstance(newvalue, (int, float)):
            self[0] = float(newvalue)
        else:
            raise TypeError("Only integer or float values can be accepted.")

    @y.setter
    def y(self, newvalue):
        """
        :param newvalue: A Vector3 instance and the value you want to change y to.
        :return: Changes y value to new value.
        """
        if isinstance(newvalue, (int, float)):
            self[1] = float(newvalue)
        else:
            raise TypeError("Only integer or float values can be accepted.")

    @z.setter
    def z(self, newvalue):
        """
        :param newvalue: A Vector3 instance and the value you want to change z to.
        :return: Changes z value to new value.
        """
        if isinstance(newvalue, (int, float)):
            self[2] = float(newvalue)
        else:
            raise TypeError("Only integer or float values can be accepted.")


def dot(v1, v2):
    """Preforming the dot product"""
    if v1.dim == v2.dim:
        i = 0
        sum = 0
        while i < v1.dim:
            d = v1[i] * v2[i]
            sum += d
            i += 1
        return sum


def cross(v1, v2):
    """Preforming the cross product"""
    if isinstance(v1 and v2, Vector3):
        x = (v1[1] * v2[2]) - (v1[2] * v2[1])
        y = (v1[2] * v2[0]) - (v1[0] * v2[2])
        z = (v1[0] * v2[1]) - (v1[1] * v2[0])
        return Vector(x, y, z)


def polar_to_Vector2(x, y, param):
    """Converting a Vector to a coordinate"""
    if param == "Yes":
        return Vector2(x, -y)
    else:
        return Vector2(x, y)
