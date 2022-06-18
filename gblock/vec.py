# -*- coding: utf-8 -*-

# majority is reworked by @prslvtsv to downgrade for py2.7

"""
MIT License

Copyright (c) 2020 João Paludo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.



"""

import math


class Vec2:
    """Represent a vector with 2 coordinates"""

    def __init__(self, x=0, y=0):
        if type(x) is list or type(x) is tuple:
            try:
                assert len(x) == 2
                self._create(*x)
            except AssertionError:
                raise ValueError("Vec2 must have exactly 2 components!")
        else:
            self._create(x, y)

    def _create(self, x, y):
        try:
            self.x = float(x)
            self.y = float(y)
        except (ValueError, TypeError) as e:
            print "Vector components must be float convertable!"

    def __str__(self):
        return "Vec2({}, {})".format(self.x, self.y)

    __repr__ = __str__

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    def __add__(self, other):
        """Add two Vec2 obejcts"""
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """Subtract two Vec2 obejcts"""
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        """Multiply the vector with a scalar"""
        if type(scalar) is not int and type(scalar) is not float:
            raise TypeError("Only scalar multiplication allow for Vec2")
        return Vec2(scalar * self.x, scalar * self.y)

    __rmul__ = __mul__

    def __truediv__(self, scalar):
        """Divide the vector by a scalar"""
        return Vec2(self.x / scalar, self.y / scalar)

    def __floordiv__(self, scalar):
        """Divide and floor the vector by a scalar"""
        return Vec2(self.x // scalar, self.y // scalar)

    def dot(self, other):
        """Return the dot product with another Vec2"""
        return self.x * other.x + self.y * other.y

    def norm(self):
        """Return the norm of the vector"""
        return math.sqrt(self.dot(self))

    def norm2(self):
        """Return the squared norm of the vector"""
        return self.dot(self)

    __abs__ = norm

    def versor(self):
        """Return the normalized vec2"""
        return self / self.norm()


class Vec3:
    """Represent a vector with 3 coordinates"""

    def __init__(self, x=0, y=0, z=0):
        if type(x) is list or type(x) is tuple:
            try:
                assert len(x) == 3
                self._create(*x)
            except AssertionError:
                raise ValueError("Vec3 must have exactly 3 components!")
        elif type(x) is Vec2:
            self._create(x.x, x.y, 0)
        else:
            self._create(x, y, z)

    def _create(self, x, y, z):
        try:
            self.x = float(x)
            self.y = float(y)
            self.z = float(z)
        except (ValueError, TypeError) as e:
            print "Vector components must be float convertable!"

    def __str__(self):
        return "Vec3({}, {}, {})".format(self.x, self.y, self.z)

    __repr__ = __str__

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __neg__(self):
        return Vec3(-self.x, -self.y, -self.z)

    def __add__(self, other):
        """Add two Vec3 obejcts"""
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        """Subtract two Vec3 obejcts"""
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        """Multiply the vector with a scalar"""
        if type(scalar) is not int and type(scalar) is not float:
            raise TypeError("Only scalar multiplication allow for Vec3")
        return Vec3(scalar * self.x, scalar * self.y, scalar * self.z)

    __rmul__ = __mul__

    def __truediv__(self, scalar):
        """Divide the vector by a scalar"""
        return Vec3(self.x / scalar, self.y / scalar, self.z / scalar)

    def __floordiv__(self, scalar):
        """Divide and floor the vector by a scalar"""
        return Vec3(self.x // scalar, self.y // scalar, self.z // scalar)

    def dot(self, other):
        """Return the dot product with another Vec3"""
        return self.x * other.x + self.y * other.y + self.z * other.z

    def norm(self):
        """Return the norm of the vector"""
        return math.sqrt(self.dot(self))

    def norm2(self):
        """Return the squared norm of the vector"""
        return self.dot(self)

    __abs__ = norm

    def versor(self):
        """Return the normalized vec3"""
        return self / self.norm()
