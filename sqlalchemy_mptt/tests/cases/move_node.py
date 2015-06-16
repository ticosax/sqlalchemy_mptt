#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 uralbash <root@uralbash.ru>
#
# Distributed under terms of the MIT license.


class MoveBefore(object):

    def test_move_before_to_top_level(self):
        """ For example move node(4) before node(1)

        initial state of the tree :mod:`sqlalchemy_mptt.tests.add_mptt_tree`

        .. code::

            level           Nested sets example
                1                    1(1)22
                        _______________|___________________
                       |               |                   |
                2    2(2)5           6(4)11             12(7)21
                       |               ^                   ^
                3    3(3)4       7(5)8   9(6)10    13(8)16   17(10)20
                                                      |          |
                4                                  14(9)15   18(11)19

            level            move 4 before 1
                1         1(4)6              1(1)16
                            ^           _______|_______
                      2(5)3   4(6)5    |               |
                2                    2(2)5           6(7)15
                                       |               ^
                3                    3(3)4      7(8)10   11(10)14
                                                  |          |
                4                               8(9)9    12(11)13

        """
        node = self.session.query(self.model).filter(self.model.ppk == 4).one()
        node.move_before(1)
        #                 id lft rgt lvl parent tree
        self.assertEqual([(1,   1, 16, 1, None, 2),
                          (2,   2,  5, 2,  1, 2),
                          (3,   3,  4, 3,  2, 2),

                          (4,   1,  6, 1,  None, 1),
                          (5,   2,  3, 2,  4, 1),
                          (6,   4,  5, 2,  4, 1),

                          (7,   6, 15, 2,  1, 2),
                          (8,   7, 10, 3,  7, 2),
                          (9,   8,  9, 4,  8, 2),
                          (10, 11, 14, 3,  7, 2),
                          (11, 12, 13, 4, 10, 2),

                          (12,  1, 22, 1, None, 3),
                          (13,  2,  5, 2, 12, 3),
                          (14,  3,  4, 3, 13, 3),
                          (15,  6, 11, 2, 12, 3),
                          (16,  7,  8, 3, 15, 3),
                          (17,  9, 10, 3, 15, 3),
                          (18, 12, 21, 2, 12, 3),
                          (19, 13, 16, 3, 18, 3),
                          (20, 14, 15, 4, 19, 3),
                          (21, 17, 20, 3, 18, 3),
                          (22, 18, 19, 4, 21, 3)], self.result.all())

    def test_move_one_tree_before_another(self):
        """ For example move node(12) before node(1)

        initial state of the tree :mod:`sqlalchemy_mptt.tests.add_mptt_tree`

        .. code::
                                        <--------------------------------
                                                                        |
            level           Nested sets tree1                           |
                1                    1(1)22                             |
                        _______________|___________________             |
                       |               |                   |            |
                2    2(2)5           6(4)11             12(7)21         |
                       |               ^                   ^            |
                3    3(3)4       7(5)8   9(6)10    13(8)16   17(10)20   |
                                                      |          |      |
                4                                  14(9)15   18(11)19   |
                                                                        |
                level           Nested sets tree2                       |
                1                    1(12)22 ----------------------------
                        _______________|___________________
                       |               |                   |
                2    2(13)5         6(15)11             12(18)21
                       |               ^                    ^
                3    3(14)4     7(16)8   9(17)10   13(19)16   17(21)20
                                                       |          |
                4                                  14(20)15   18(22)19

        """
        node = self.session.query(self.model)\
            .filter(self.model.ppk == 12).one()
        node.move_before("1")
        #                 id lft rgt lvl parent tree
        self.assertEqual([(1,   1, 22, 1, None, 2),
                          (2,   2,  5, 2,  1, 2),
                          (3,   3,  4, 3,  2, 2),
                          (4,   6, 11, 2,  1, 2),
                          (5,   7,  8, 3,  4, 2),
                          (6,   9, 10, 3,  4, 2),
                          (7,  12, 21, 2,  1, 2),
                          (8,  13, 16, 3,  7, 2),
                          (9,  14, 15, 4,  8, 2),
                          (10, 17, 20, 3,  7, 2),
                          (11, 18, 19, 4, 10, 2),

                          (12,  1, 22, 1, None, 1),
                          (13,  2,  5, 2, 12, 1),
                          (14,  3,  4, 3, 13, 1),
                          (15,  6, 11, 2, 12, 1),
                          (16,  7,  8, 3, 15, 1),
                          (17,  9, 10, 3, 15, 1),
                          (18, 12, 21, 2, 12, 1),
                          (19, 13, 16, 3, 18, 1),
                          (20, 14, 15, 4, 19, 1),
                          (21, 17, 20, 3, 18, 1),
                          (22, 18, 19, 4, 21, 1)], self.result.all())

    def test_move_before_function(self):
        """ For example move node(8) before node(4)

        initial state of the tree :mod:`sqlalchemy_mptt.tests.add_mptt_tree`

        .. code::

            level           Nested sets example
            1                    1(1)22
                    _______________|___________________
                   |               |                   |
            2    2(2)5           6(4)11             12(7)21
                   |               ^                   ^
            3    3(3)4       7(5)8   9(6)10    13(8)16   17(10)20
                                                  |          |
            4                                  14(9)15   18(11)19

            level           move 8 before 4
            1                    1(1)22
                    _______________|___________________
                   |        |            |             |
            2    2(2)5    6(8)9       10(4)15       16(7)21
                   |        |            ^             |
            3    3(3)4    7(9)8   11(5)12 13(6)14  17(10)20
                                                       |
            4                                      18(11)19

        """
        node = self.session.query(self.model).filter(self.model.ppk == 8).one()
        node.move_before("4")
        #                 id lft rgt lvl parent tree
        self.assertEqual([(1,   1, 22, 1, None, 1),
                          (2,   2,  5, 2,  1, 1),
                          (3,   3,  4, 3,  2, 1),
                          (4,  10, 15, 2,  1, 1),
                          (5,  11, 12, 3,  4, 1),
                          (6,  13, 14, 3,  4, 1),
                          (7,  16, 21, 2,  1, 1),
                          (8,   6,  9, 2,  1, 1),
                          (9,   7,  8, 3,  8, 1),
                          (10, 17, 20, 3,  7, 1),
                          (11, 18, 19, 4, 10, 1),

                          (12,  1, 22, 1, None, 2),
                          (13,  2,  5, 2, 12, 2),
                          (14,  3,  4, 3, 13, 2),
                          (15,  6, 11, 2, 12, 2),
                          (16,  7,  8, 3, 15, 2),
                          (17,  9, 10, 3, 15, 2),
                          (18, 12, 21, 2, 12, 2),
                          (19, 13, 16, 3, 18, 2),
                          (20, 14, 15, 4, 19, 2),
                          (21, 17, 20, 3, 18, 2),
                          (22, 18, 19, 4, 21, 2)], self.result.all())

    def test_move_one_tree_before_other_tree(self):
        node = self.session.query(self.model).\
            filter(self.model.ppk == 12).one()
        node.move_before("1")
        #                 id lft rgt lvl parent tree
        self.assertEqual([(1,   1, 22, 1, None, 2),
                          (2,   2,  5, 2,  1, 2),
                          (3,   3,  4, 3,  2, 2),
                          (4,   6, 11, 2,  1, 2),
                          (5,   7,  8, 3,  4, 2),
                          (6,   9, 10, 3,  4, 2),
                          (7,  12, 21, 2,  1, 2),
                          (8,  13, 16, 3,  7, 2),
                          (9,  14, 15, 4,  8, 2),
                          (10, 17, 20, 3,  7, 2),
                          (11, 18, 19, 4, 10, 2),

                          (12,  1, 22, 1, None, 1),
                          (13,  2,  5, 2, 12, 1),
                          (14,  3,  4, 3, 13, 1),
                          (15,  6, 11, 2, 12, 1),
                          (16,  7,  8, 3, 15, 1),
                          (17,  9, 10, 3, 15, 1),
                          (18, 12, 21, 2, 12, 1),
                          (19, 13, 16, 3, 18, 1),
                          (20, 14, 15, 4, 19, 1),
                          (21, 17, 20, 3, 18, 1),
                          (22, 18, 19, 4, 21, 1)], self.result.all())

    def test_move_before_to_other_tree(self):
        """ For example move node(8) before node(15)

        initial state of the tree :mod:`sqlalchemy_mptt.tests.add_mptt_tree`

        .. code::

            level           Move 8 before 15
            1                    1(1)18
                     _______________|___________________
                    |               |                   |
            2     2(2)5           6(4)11             12(7)17
                    |               ^                   |
            3     3(3)4       7(5)8   9(6)10        13(10)16
                                                        |
            4                                       14(11)15

            level
            1                    1(12)26
                     _______________|______________________________
                    |         |               |                    |
            2    2(13)5     6(8)9         10(15)15             16(18)25
                    |         |               ^                    ^
            3    3(14)4     7(9)8    11(16)12  13(17)14   17(19)20   21(21)24
                                                              |          |
            4                                             18(20)19   22(22)23

        """
        node = self.session.query(self.model).filter(self.model.ppk == 8).one()
        node.move_before("15")
        #                 id lft rgt lvl parent tree
        self.assertEqual([(1,   1, 18, 1, None, 1),
                          (2,   2,  5, 2,  1, 1),
                          (3,   3,  4, 3,  2, 1),
                          (4,   6, 11, 2,  1, 1),
                          (5,   7,  8, 3,  4, 1),
                          (6,   9, 10, 3,  4, 1),
                          (7,  12, 17, 2,  1, 1),

                          (8,   6,  9, 2,  12, 2),
                          (9,   7,  8, 3,   8, 2),

                          (10, 13, 16, 3,  7, 1),
                          (11, 14, 15, 4, 10, 1),

                          (12,  1, 26, 1, None, 2),
                          (13,  2,  5, 2, 12, 2),
                          (14,  3,  4, 3, 13, 2),
                          (15, 10, 15, 2, 12, 2),
                          (16, 11, 12, 3, 15, 2),
                          (17, 13, 14, 3, 15, 2),
                          (18, 16, 25, 2, 12, 2),
                          (19, 17, 20, 3, 18, 2),
                          (20, 18, 19, 4, 19, 2),
                          (21, 21, 24, 3, 18, 2),
                          (22, 22, 23, 4, 21, 2)], self.result.all())




class MoveAfter(object):

    def test_move_after_function(self):
        """ For example move node(8) after node(5)

        initial state of the tree :mod:`sqlalchemy_mptt.tests.add_mptt_tree`

        .. code::

                level               Initial state
                    1                    1(1)22
                            _______________|___________________
                           |               |                   |
                    2    2(2)5           6(4)11             12(7)21
                           |               ^                   ^
                    3    3(3)4       7(5)8   9(6)10    13(8)16   17(10)20
                                                          |          |
                    4                                  14(9)15   18(11)19

                level               Move 8 after 5
                    1                     1(1)22
                            _______________|__________________
                           |               |                  |
                    2     2(2)5           6(4)15            16(7)21
                            |               ^                  |
                    3     3(3)4    7(5)8  9(8)12  13(6)14   17(10)20
                                            |                  |
                    4                    10(9)11            18(11)19

        """
        node = self.session.query(self.model).filter(self.model.ppk == 8).one()
        node.move_after("5")
        #                 id lft rgt lvl parent tree
        self.assertEqual([(1,   1, 22, 1, None, 1),
                          (2,   2,  5, 2,  1, 1),
                          (3,   3,  4, 3,  2, 1),
                          (4,   6, 15, 2,  1, 1),
                          (5,   7,  8, 3,  4, 1),
                          (6,  13, 14, 3,  4, 1),
                          (7,  16, 21, 2,  1, 1),
                          (8,   9, 12, 3,  4, 1),
                          (9,  10, 11, 4,  8, 1),
                          (10, 17, 20, 3,  7, 1),
                          (11, 18, 19, 4, 10, 1),

                          (12,  1, 22, 1, None, 2),
                          (13,  2,  5, 2, 12, 2),
                          (14,  3,  4, 3, 13, 2),
                          (15,  6, 11, 2, 12, 2),
                          (16,  7,  8, 3, 15, 2),
                          (17,  9, 10, 3, 15, 2),
                          (18, 12, 21, 2, 12, 2),
                          (19, 13, 16, 3, 18, 2),
                          (20, 14, 15, 4, 19, 2),
                          (21, 17, 20, 3, 18, 2),
                          (22, 18, 19, 4, 21, 2)], self.result.all())

    def test_move_to_toplevel_where_much_trees_from_right_side(self):
        """ Move 20 after 1

        initial state of the tree :mod:`sqlalchemy_mptt.tests.add_mptt_tree`

        .. code::

            level           tree_id = 1
            1                    1(1)22
                    _______________|___________________
                   |               |                   |
            2    2(2)5           6(4)11             12(7)21
                   |               ^                   ^
            3    3(3)4       7(5)8   9(6)10    13(8)16   17(10)20
                                                  |          |
            4                                  14(9)15   18(11)19

            level           tree_id = 2
            1                     1(15)6
                                     ^
            2                 2(16)3   4(17)5

            level           tree_id = 3
            1                    1(12)16
                     _______________|
                    |               |
            2    2(13)5          6(18)15
                    |               ^
            3    3(14)4     7(19)10   11(21)14
                               |          |
            4               8(20)9    12(22)13

        """
        node = self.session.query(self.model)\
            .filter(self.model.ppk == 15).one()
        node.move_after("1")
        #                 id lft rgt lvl parent tree
        self.assertEqual([(1,   1, 22, 1, None, 1),
                          (2,   2,  5, 2,  1, 1),
                          (3,   3,  4, 3,  2, 1),
                          (4,   6, 11, 2,  1, 1),
                          (5,   7,  8, 3,  4, 1),
                          (6,   9, 10, 3,  4, 1),
                          (7,  12, 21, 2,  1, 1),
                          (8,  13, 16, 3,  7, 1),
                          (9,  14, 15, 4,  8, 1),
                          (10, 17, 20, 3,  7, 1),
                          (11, 18, 19, 4, 10, 1),

                          (12, 1, 16, 1, None, 3),
                          (13, 2,  5, 2, 12,   3),
                          (14, 3,  4, 3, 13,   3),

                          (15, 1, 6, 1, None, 2),
                          (16, 2, 3, 2, 15,   2),
                          (17, 4, 5, 2, 15,   2),

                          (18,  6, 15, 2, 12, 3),
                          (19,  7, 10, 3, 18, 3),
                          (20,  8,  9, 4, 19, 3),
                          (21, 11, 14, 3, 18, 3),
                          (22, 12, 13, 4, 21, 3)], self.result.all())

        node = self.session.query(self.model)\
            .filter(self.model.ppk == 20).one()
        node.move_after("1")
        """ level           tree_id = 1
            1                    1(1)22
                    _______________|___________________
                   |               |                   |
            2    2(2)5           6(4)11             12(7)21
                   |               ^                   ^
            3    3(3)4       7(5)8   9(6)10    13(8)16   17(10)20
                                                  |          |
            4                                  14(9)15   18(11)19

            level           tree_id = 2
            1                   1(20)2

            level           tree_id = 3
            1                     1(15)6
                                     ^
            2                 2(16)3   4(17)5

            level           tree_id = 4
            1                    1(12)14
                     _______________|
                    |               |
            2    2(13)5          6(18)13
                    |               ^
            3    3(14)4     7(19)8     9(21)12
                                          |
            4                         10(22)11

        """
        #                 id lft rgt lvl parent tree
        self.assertEqual([(1,   1, 22, 1, None, 1),
                          (2,   2,  5, 2,  1, 1),
                          (3,   3,  4, 3,  2, 1),
                          (4,   6, 11, 2,  1, 1),
                          (5,   7,  8, 3,  4, 1),
                          (6,   9, 10, 3,  4, 1),
                          (7,  12, 21, 2,  1, 1),
                          (8,  13, 16, 3,  7, 1),
                          (9,  14, 15, 4,  8, 1),
                          (10, 17, 20, 3,  7, 1),
                          (11, 18, 19, 4, 10, 1),

                          (12, 1, 14, 1, None, 4),
                          (13, 2,  5, 2, 12,   4),
                          (14, 3,  4, 3, 13,   4),

                          (15, 1, 6, 1, None, 3),
                          (16, 2, 3, 2, 15,   3),
                          (17, 4, 5, 2, 15,   3),

                          (18,  6, 13, 2, 12, 4),
                          (19,  7,  8, 3, 18, 4),
                          (20,  1,  2, 1, None, 2),
                          (21,  9, 12, 3, 18, 4),
                          (22, 10, 11, 4, 21, 4)], self.result.all())

    def test_move_to_toplevel(self):
        """ Move node(8) to top level after node(1)

        initial state of the tree :mod:`sqlalchemy_mptt.tests.add_mptt_tree`

        .. code::

            level           Nested sets example
                1                    1(1)22
                        _______________|___________________
                       |               |                   |
                2    2(2)5           6(4)11             12(7)21
                       |               ^                   ^
                3    3(3)4       7(5)8   9(6)10    13(8)16   17(10)20
                                                      |          |
                4                                  14(9)15   18(11)19

            level               Move 8 after 1
                1                     1(1)18                     1(8)4
                         _______________|______________            |
                        |               |              |           |
                2     2(2)5           6(4)11        12(7)17      2(9)3
                        |               ^              |
                3     3(3)4       7(5)8   9(6)10   13(10)16
                                                       |
                4                                  14(11)15

        """
        node = self.session.query(self.model).filter(self.model.ppk == 8).one()
        node.move_after("1")
        #                 id lft rgt lvl parent tree
        self.assertEqual([(1,   1, 18, 1, None, 1),
                          (2,   2,  5, 2,  1, 1),
                          (3,   3,  4, 3,  2, 1),
                          (4,   6, 11, 2,  1, 1),
                          (5,   7,  8, 3,  4, 1),
                          (6,   9, 10, 3,  4, 1),
                          (7,  12, 17, 2,  1, 1),

                          (8,   1,  4, 1, None, 2),
                          (9,   2,  3, 2,  8, 2),

                          (10, 13, 16, 3,  7, 1),
                          (11, 14, 15, 4, 10, 1),

                          (12,  1, 22, 1, None, 3),
                          (13,  2,  5, 2, 12, 3),
                          (14,  3,  4, 3, 13, 3),
                          (15,  6, 11, 2, 12, 3),
                          (16,  7,  8, 3, 15, 3),
                          (17,  9, 10, 3, 15, 3),
                          (18, 12, 21, 2, 12, 3),
                          (19, 13, 16, 3, 18, 3),
                          (20, 14, 15, 4, 19, 3),
                          (21, 17, 20, 3, 18, 3),
                          (22, 18, 19, 4, 21, 3)], self.result.all())

    def test_move_to_toplevel2(self):
        """ Move node(8) to top level after node(1)

        initial state of the tree :mod:`sqlalchemy_mptt.tests.add_mptt_tree`

        .. code::

            level           Nested sets example
                1                    1(1)22
                        _______________|___________________
                       |               |                   |
                2    2(2)5           6(4)11             12(7)21
                       |               ^                   ^
                3    3(3)4       7(5)8   9(6)10    13(8)16   17(10)20
                                                      |          |
                4                                  14(9)15   18(11)19

            level               Move 8 after 1
                1                     1(1)18                     1(8)4
                         _______________|______________            |
                        |               |              |           |
                2     2(2)5           6(4)11        12(7)17      2(9)3
                        |               ^              |
                3     3(3)4       7(5)8   9(6)10   13(10)16
                                                       |
                4                                  14(11)15

                          id lft rgt lvl parent tree
        """
        node = self.session.query(self.model).filter(self.model.ppk == 8).one()
        node.parent_id = None
        self.session.add(node)
        #                 id lft rgt lvl parent tree
        self.assertEqual([(1,   1, 18, 1, None, 1),
                          (2,   2,  5, 2,  1, 1),
                          (3,   3,  4, 3,  2, 1),
                          (4,   6, 11, 2,  1, 1),
                          (5,   7,  8, 3,  4, 1),
                          (6,   9, 10, 3,  4, 1),
                          (7,  12, 17, 2,  1, 1),

                          (8,   1,  4, 1, None, 3),
                          (9,   2,  3, 2,  8, 3),

                          (10, 13, 16, 3,  7, 1),
                          (11, 14, 15, 4, 10, 1),

                          (12,  1, 22, 1, None, 2),
                          (13,  2,  5, 2, 12, 2),
                          (14,  3,  4, 3, 13, 2),
                          (15,  6, 11, 2, 12, 2),
                          (16,  7,  8, 3, 15, 2),
                          (17,  9, 10, 3, 15, 2),
                          (18, 12, 21, 2, 12, 2),
                          (19, 13, 16, 3, 18, 2),
                          (20, 14, 15, 4, 19, 2),
                          (21, 17, 20, 3, 18, 2),
                          (22, 18, 19, 4, 21, 2)], self.result.all())

    def test_move_to_toplevel_big_subtree(self):
        """ Move node(7) (big subtree) to top level after node(1)

        initial state of the tree :mod:`sqlalchemy_mptt.tests.add_mptt_tree`

        .. code::

            level           Nested sets example
                1                    1(1)22
                        _______________|___________________
                       |               |                   |
                2    2(2)5           6(4)11             12(7)21
                       |               ^                   ^
                3    3(3)4       7(5)8   9(6)10    13(8)16   17(10)20
                                                      |          |
                4                                  14(9)15   18(11)19

            level               Move 7 to toplevel
                1                     1(1)12             1(7)10
                         _______________|              ____|____
                        |               |             |         |
                2     2(2)5           6(4)11        2(8)5     6(10)9
                        |               ^             |         |
                3     3(3)4       7(5)8   9(6)10    3(9)4     7(11)8

                          id lft rgt lvl parent tree
        """
        node = self.session.query(self.model).filter(self.model.ppk == 7).one()
        node.parent_id = None
        self.session.add(node)
        #                 id lft rgt lvl parent tree
        self.assertEqual([(1,   1, 12, 1, None, 1),
                          (2,   2,  5, 2,  1, 1),
                          (3,   3,  4, 3,  2, 1),
                          (4,   6, 11, 2,  1, 1),
                          (5,   7,  8, 3,  4, 1),
                          (6,   9, 10, 3,  4, 1),

                          (7,   1, 10, 1, None, 3),
                          (8,   2,  5, 2,  7,   3),
                          (9,   3,  4, 3,  8,   3),
                          (10,  6,  9, 2,  7,   3),
                          (11,  7,  8, 3, 10,   3),

                          (12,  1, 22, 1, None, 2),
                          (13,  2,  5, 2, 12, 2),
                          (14,  3,  4, 3, 13, 2),
                          (15,  6, 11, 2, 12, 2),
                          (16,  7,  8, 3, 15, 2),
                          (17,  9, 10, 3, 15, 2),
                          (18, 12, 21, 2, 12, 2),
                          (19, 13, 16, 3, 18, 2),
                          (20, 14, 15, 4, 19, 2),
                          (21, 17, 20, 3, 18, 2),
                          (22, 18, 19, 4, 21, 2)], self.result.all())

    def test_move_after_between_tree(self):
        """ Move node(7) (big subtree) to top level after node(1) and before node(12)

        initial state of the tree :mod:`sqlalchemy_mptt.tests.add_mptt_tree`

        .. code::

            level           Nested sets example
                1                    1(1)22
                        _______________|___________________
                       |               |                   |
                2    2(2)5           6(4)11             12(7)21
                       |               ^                   ^
                3    3(3)4       7(5)8   9(6)10    13(8)16   17(10)20
                                                      |          |
                4                                  14(9)15   18(11)19

            level               Move 7 to toplevel
                1                     1(1)12             1(7)10
                         _______________|              ____|____
                        |               |             |         |
                2     2(2)5           6(4)11        2(8)5     6(10)9
                        |               ^             |         |
                3     3(3)4       7(5)8   9(6)10    3(9)4     7(11)8

                          id lft rgt lvl parent tree
        """
        node = self.session.query(self.model).filter(self.model.ppk == 7).one()
        node.move_after("1")
        #                 id lft rgt lvl parent tree
        self.assertEqual([(1,   1, 12, 1, None, 1),
                          (2,   2,  5, 2,  1, 1),
                          (3,   3,  4, 3,  2, 1),
                          (4,   6, 11, 2,  1, 1),
                          (5,   7,  8, 3,  4, 1),
                          (6,   9, 10, 3,  4, 1),

                          (7,   1, 10, 1, None, 2),
                          (8,   2,  5, 2,  7,   2),
                          (9,   3,  4, 3,  8,   2),
                          (10,  6,  9, 2,  7,   2),
                          (11,  7,  8, 3, 10,   2),

                          (12,  1, 22, 1, None, 3),
                          (13,  2,  5, 2, 12, 3),
                          (14,  3,  4, 3, 13, 3),
                          (15,  6, 11, 2, 12, 3),
                          (16,  7,  8, 3, 15, 3),
                          (17,  9, 10, 3, 15, 3),
                          (18, 12, 21, 2, 12, 3),
                          (19, 13, 16, 3, 18, 3),
                          (20, 14, 15, 4, 19, 3),
                          (21, 17, 20, 3, 18, 3),
                          (22, 18, 19, 4, 21, 3)], self.result.all())


class MoveInside(object):

    def test_move_between_tree(self):
        """ Move node(4) to other tree inside node(15)

        initial state of the tree :mod:`sqlalchemy_mptt.tests.add_mptt_tree`

        .. code::

            level           Nested sets tree1
            1                    1(1)16
                    _______________|_____________________
                   |                                     |
            2    2(2)5                                 6(7)15
                   |                                     ^
            3    3(3)4                            7(8)10   11(10)14
                                                    |          |
            4                                     8(9)9    12(11)13

            level           Nested sets tree2
            1                     1(12)28
                     ________________|_______________________
                    |                |                       |
            2    2(13)5            6(15)17                18(18)27
                   |                 ^                        ^
            3    3(14)4    7(4)12 13(16)14  15(17)16  19(19)22  23(21)26
                             ^                            |         |
            4          8(5)9  10(6)11                 20(20)21  24(22)25

        """
        node = self.session.query(self.model).filter(self.model.ppk == 4).one()
        node.parent_id = 15
        self.session.add(node)
        #                 id lft rgt lvl parent tree
        self.assertEqual([(1,   1, 16, 1, None, 1),
                          (2,   2,  5, 2,   1,  1),
                          (3,   3,  4, 3,   2,  1),

                          (4,   7, 12, 3,  15, 2),
                          (5,   8,  9, 4,   4, 2),
                          (6,  10, 11, 4,   4, 2),

                          (7,   6, 15, 2,   1,  1),
                          (8,   7, 10, 3,   7,  1),
                          (9,   8,  9, 4,   8,  1),
                          (10, 11, 14, 3,   7,  1),
                          (11, 12, 13, 4,  10,  1),

                          (12,  1, 28, 1, None, 2),
                          (13,  2,  5, 2, 12, 2),
                          (14,  3,  4, 3, 13, 2),
                          (15,  6, 17, 2, 12, 2),
                          (16, 13, 14, 3, 15, 2),
                          (17, 15, 16, 3, 15, 2),
                          (18, 18, 27, 2, 12, 2),
                          (19, 19, 22, 3, 18, 2),
                          (20, 20, 21, 4, 19, 2),
                          (21, 23, 26, 3, 18, 2),
                          (22, 24, 25, 4, 21, 2)], self.result.all())

    def test_move_tree_to_another_tree(self):
        """ Move tree(2) inside tree(1)

        initial state of the tree :mod:`sqlalchemy_mptt.tests.add_mptt_tree`

        .. code::

            level           Move tree2 to tree1
            1                    1(1)44
                     _______________|_________________________________
                    |               |                                 |
            2     2(2)5           6(4)11                            12(7)43
                    |            ___|___                             __|_____________________________________
                    |           |       |                           |                             |          |
            3     3(3)4       7(5)8   9(6)10                    13(12)34                       35(8)38   39(10)42
                                                    _______________|___________________           |          |
                                                   |               |                   |       36(9)37   40(11)41
            4                                   14(13)17        18(15)23             24(18)33
                                                    |               ^                    ^
            5                                   15(14)16   19(16)20   21(17)22   25(19)28  29(21)32
                                                                                     |         |
            6                                                                    26(20)27  30(22)31

        """  # noqa
        node = self.session.query(self.model).\
            filter(self.model.ppk == 12).one()
        node.parent_id = 7
        self.session.add(node)
        #                 id lft rgt lvl parent tree
        self.assertEqual([(1, 1, 44, 1, None, 1),
                          (2, 2, 5, 2, 1, 1),
                          (3, 3, 4, 3, 2, 1),
                          (4, 6, 11, 2, 1, 1),
                          (5, 7, 8, 3, 4, 1),
                          (6, 9, 10, 3, 4, 1),
                          (7, 12, 43, 2, 1, 1),
                          (8, 35, 38, 3, 7, 1),
                          (9, 36, 37, 4, 8, 1),
                          (10, 39, 42, 3, 7, 1),
                          (11, 40, 41, 4, 10, 1),
                          (12, 13, 34, 3, 7, 1),
                          (13, 14, 17, 4, 12, 1),
                          (14, 15, 16, 5, 13, 1),
                          (15, 18, 23, 4, 12, 1),
                          (16, 19, 20, 5, 15, 1),
                          (17, 21, 22, 5, 15, 1),
                          (18, 24, 33, 4, 12, 1),
                          (19, 25, 28, 5, 18, 1),
                          (20, 26, 27, 6, 19, 1),
                          (21, 29, 32, 5, 18, 1),
                          (22, 30, 31, 6, 21, 1)], self.result.all())

    def test_move_inside_function(self):
        """ For example move node(4) inside node(15)

        initial state of the tree :mod:`sqlalchemy_mptt.tests.add_mptt_tree`

        .. code::

            level           Nested sets tree1
            1                    1(1)16
                    _______________|_____________________
                   |                                     |
            2    2(2)5                                 6(7)15
                   |                                     ^
            3    3(3)4                            7(8)10   11(10)14
                                                    |          |
            4                                     8(9)9    12(11)13

            level           Nested sets tree2
            1                     1(12)28
                     ________________|_______________________
                    |                |                       |
            2    2(13)5            6(15)17                18(18)27
                   |                 ^                        ^
            3    3(14)4    7(4)12 13(16)14  15(17)16  19(19)22  23(21)26
                             ^                            |         |
            4          8(5)9  10(6)11                 20(20)21  24(22)25

        """
        node = self.session.query(self.model).filter(self.model.ppk == 4).one()
        node.move_inside("15")
        #                 id lft rgt lvl parent tree
        self.assertEqual([(1,   1, 16, 1, None, 1),
                          (2,   2,  5, 2,   1,  1),
                          (3,   3,  4, 3,   2,  1),

                          (4,   7, 12, 3,  15, 2),
                          (5,   8,  9, 4,   4, 2),
                          (6,  10, 11, 4,   4, 2),

                          (7,   6, 15, 2,   1,  1),
                          (8,   7, 10, 3,   7,  1),
                          (9,   8,  9, 4,   8,  1),
                          (10, 11, 14, 3,   7,  1),
                          (11, 12, 13, 4,  10,  1),

                          (12,  1, 28, 1, None, 2),
                          (13,  2,  5, 2, 12, 2),
                          (14,  3,  4, 3, 13, 2),
                          (15,  6, 17, 2, 12, 2),
                          (16, 13, 14, 3, 15, 2),
                          (17, 15, 16, 3, 15, 2),
                          (18, 18, 27, 2, 12, 2),
                          (19, 19, 22, 3, 18, 2),
                          (20, 20, 21, 4, 19, 2),
                          (21, 23, 26, 3, 18, 2),
                          (22, 24, 25, 4, 21, 2)], self.result.all())

    def test_tree_shorting(self):
        """ Try to move top level node(1) inside tree

        .. code::

            level           Nested sets example
            1                    1(1)22
                    _______________|___________________
                   |               |                   |
            2    2(2)5           6(4)11             12(7)21
                   |               ^                   ^
            3    3(3)4       7(5)8   9(6)10    13(8)16   17(10)20
                                                  |          |
            4                                  14(9)15   18(11)19

            level           Nested sets example

                                    __parent_id______________________
                                   |                                 |
            1                    1(1)22                              |
                    _______________|___________________              |
                   |               |                   |             |
            2    2(2)5           6(4)11             12(7)21         (X)
                   |               ^                   ^             |
            3    3(3)4       7(5)8   9(6)10    13(8)16   17(10)20    |
                                                  |          |       |
            4                                  14(9)15   18(11)19    |
                                                            ↑        |
                                                            ↑________|
        """
        node = self.session.query(self.model).filter(self.model.ppk == 1).one()
        node.parent_id = 11
        self.session.add(node)
        #                 id lft rgt lvl parent tree
        self.assertEqual([(1,   1, 22, 1, None, 1),
                          (2,   2,  5, 2,  1, 1),
                          (3,   3,  4, 3,  2, 1),
                          (4,   6, 11, 2,  1, 1),
                          (5,   7,  8, 3,  4, 1),
                          (6,   9, 10, 3,  4, 1),
                          (7,  12, 21, 2,  1, 1),
                          (8,  13, 16, 3,  7, 1),
                          (9,  14, 15, 4,  8, 1),
                          (10, 17, 20, 3,  7, 1),
                          (11, 18, 19, 4, 10, 1),

                          (12,  1, 22, 1, None, 2),
                          (13,  2,  5, 2, 12, 2),
                          (14,  3,  4, 3, 13, 2),
                          (15,  6, 11, 2, 12, 2),
                          (16,  7,  8, 3, 15, 2),
                          (17,  9, 10, 3, 15, 2),
                          (18, 12, 21, 2, 12, 2),
                          (19, 13, 16, 3, 18, 2),
                          (20, 14, 15, 4, 19, 2),
                          (21, 17, 20, 3, 18, 2),
                          (22, 18, 19, 4, 21, 2)], self.result.all())

    def test_move_inside_to_the_same_parent_function(self):
        """ For example move node(6) inside node(4)

        initial state of the tree :mod:`sqlalchemy_mptt.tests.add_mptt_tree`

        .. code::

            level               Initial state
                1                    1(1)22
                        _______________|___________________
                       |               |                   |
                2    2(2)5           6(4)11             12(7)21
                       |               ^                   ^
                3    3(3)4       7(5)8   9(6)10    13(8)16   17(10)20
                                                      |          |
                4                                  14(9)15   18(11)19

            level           move 6 inside 4
                1                    1(1)22
                        _______________|___________________
                       |               |                   |
                2    2(2)5           6(4)11             12(7)21
                       |               ^                   ^
                3    3(3)4       7(6)8   9(5)10    13(8)16   17(10)20
                                                      |          |
                4                                  14(9)15   18(11)19

        """
        node = self.session.query(self.model).filter(self.model.ppk == 6).one()
        node.move_inside("4")
        #                 id lft rgt lvl parent tree
        self.assertEqual([(1,   1, 22, 1, None, 1),
                          (2,   2,  5, 2,  1, 1),
                          (3,   3,  4, 3,  2, 1),
                          (4,   6, 11, 2,  1, 1),
                          (5,   9, 10, 3,  4, 1),
                          (6,   7,  8, 3,  4, 1),
                          (7,  12, 21, 2,  1, 1),
                          (8,  13, 16, 3,  7, 1),
                          (9,  14, 15, 4,  8, 1),
                          (10, 17, 20, 3,  7, 1),
                          (11, 18, 19, 4, 10, 1),

                          (12,  1, 22, 1, None, 2),
                          (13,  2,  5, 2, 12, 2),
                          (14,  3,  4, 3, 13, 2),
                          (15,  6, 11, 2, 12, 2),
                          (16,  7,  8, 3, 15, 2),
                          (17,  9, 10, 3, 15, 2),
                          (18, 12, 21, 2, 12, 2),
                          (19, 13, 16, 3, 18, 2),
                          (20, 14, 15, 4, 19, 2),
                          (21, 17, 20, 3, 18, 2),
                          (22, 18, 19, 4, 21, 2)], self.result.all())
