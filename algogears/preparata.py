from .core import Point, ThreadedBinTreeNode, ThreadedBinTree, PointType, PathDirection


class PreparataNode(ThreadedBinTreeNode):
    @property
    def point(self):
        return self.data
    
    @point.setter
    def point(self, value):
        self.data = value
    
    @point.deleter
    def point(self):
        del self.data


class PreparataThreadedBinTree(ThreadedBinTree):
    node_class = PreparataNode


def preparata(points):
    points.sort()

    if len(points) < 3:
        yield points
    else:
        # Find first three non-collinear points
        i = 2
        while Point.direction(points[0], points[1], points[i]) == 0:
            i += 1
        
        # Insert 3rd point in the correct position
        point3 = points[i]
        del points[i]
        points.insert(2, point3)

        hulls, trees, left_paths, left_supporting_points, right_paths, right_supporting_points, deleted_points = [], [], [], [], [], [], []

        # Construct the initial hull clockwise, starting from the leftmost point
        hull = [points[0]] + sorted(points[1:3], key=lambda p: -Point.polar_angle(p, points[0]))
        hulls.append(hull)

        for point in points[3:]:
            tree = PreparataThreadedBinTree.from_iterable(hull)
            trees.append(tree)

            left_supporting_path, left_supporting_point = find_path_to_supporting_point(tree, point, search_left_supporting=True)
            right_supporting_path, right_supporting_point = find_path_to_supporting_point(tree, point, search_left_supporting=False)
            left_paths.append(left_supporting_path)
            right_paths.append(right_supporting_path)
            left_supporting_points.append(left_supporting_point)
            right_supporting_points.append(right_supporting_point)
            
            left_i = hull.index(left_supporting_point)
            right_i = hull.index(right_supporting_point)
            
            # Drop the points from exclusive range (right, left) and insert the new point between right and left.
            deleted_points.append(hull[right_i+1:] if left_i < right_i else hull[right_i+1:left_i])
            hull = hull[:right_i+1] + [point] + ([] if left_i < right_i else hull[left_i:])
            hulls.append(hull)
        
        yield hulls[0], trees[0]
        yield (left_paths, left_supporting_points), (right_paths, right_supporting_points)
        yield deleted_points
        yield hulls[1:], trees[1:]
        yield hull


def find_path_to_supporting_point(tree, point, search_left_supporting):
    path = []
    node, prev = tree.root, None
    
    while prev != node:
        prev = node
        node = find_next_node(node, point, search_left_supporting)
        
        if node is not prev:
            path.append(PathDirection.left if node is prev.prev else PathDirection.right)
    
    return path, node.point


def find_next_node(node, point, search_left_supporting):
    point_type = PointType.by_points(point, node.point, node.prev.point, node.next.point)
    match point_type:
        case PointType.convex:
            return node.next if search_left_supporting else node.prev
        case PointType.reflex:
            return node.prev if search_left_supporting else node.next
        case PointType.left_supporting:
            return node if search_left_supporting else node.prev
        case PointType.right_supporting:
            return node.next if search_left_supporting else node
