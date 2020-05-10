type List = NonEmpty of Any * List or Empty
type Coord = Point of float * float or LineCoords of Point * Point
type Shape = Line of float * float * float

let list_fold_left fun acc list =
    match list with
    |   Empty -> acc
    |   NonEmpty head tail ->
            list_fold_left fun (fun acc head) tail
    end

let rectangle left_bottom right_upper =
    fn point ->
        match left_bottom with
            Point x1 y1 ->
                match right_upper with
                    Point x2 y2 ->
                        match point with
                            Point x y ->
                                if x1 <= x and x <= x2 and y1 <= y and y <= y2 then
                                    1
                                else
                                    0
                        end
                end
        end

let circle center radius =
    fn point ->
        match center with
            Point x1 y1 ->
                match point with
                    Point x y ->
                        if ((x1 - x) ^ 2 + (y1 - y) ^ 2) ^ 0.5 <= radius then
                            1
                        else
                            0
                end
        end

let make_line point1 point2 =
    match point1 with
        Point x1 y1 ->
            match point2 with
                Point x2 y2 ->
                    let a = y1 - y2 in
                    let b = x2 - x1 in
                    let c = -y1 * b - x1 * a in
                    Line a b c
            end
    end

let line_side line point =
    match line with
        Line a b c ->
            match point with
                Point x y ->
                    a * x + b * y + c
            end
    end

let denominator a b =
    (a ^ 2) + (b ^ 2)

let flip_x line point =
    match line with
        Line a b c ->
            match point with
                Point x y ->
                    let numerator = ((b ^ 2) - (a ^ 2)) * x - 2 * a * b * y  - 2 * a * c in
                    numerator / denominator a b
            end
    end

let flip_y line point =
    match line with
        Line a b c ->
            match point with
                Point x y ->
                    let numerator = ((a ^ 2) - (b ^ 2)) * y - 2 * a * b * y  - 2 * b * c in
                    numerator / denominator a b
            end
    end

let points_after_fold line point =
    let side = line_side line point in
    if side == 0 then
        NonEmpty point Empty
    elif side < 0 then
        Empty
    else
        let x = flip_x line point in
        let y = flip_y line point in
        NonEmpty point (NonEmpty (Point x y) Empty)

let fold point1 point2 paper =
    fn point ->
        let count acc pnt = acc + paper pnt in
        let line = make_line point1 point2 in
        let points = points_after_fold line point in
        list_fold_left count 0 points

let multi_fold lines paper =
    let fold_helper acc points =
        match points with
            LineCoords point1 point2 ->
                fold point1 point2 acc
        end
    in
        list_fold_left fold_helper paper lines

let test_rect1 = rectangle (Point 0 0) (Point 2 2) (Point 2 0) == 1
let test_rect2 = rectangle (Point 0 0) (Point 2 2) (Point (-1) 1) == 0

let test_circle1 = circle (Point 0 0) 2 (Point 2 0) == 1
let test_circle2 = circle (Point 0 0) 2 (Point (-1) 1) == 1
let test_circle3 = circle (Point 0 0) 2 (Point (-1) 2) == 0

let crcl = circle (Point 0 0) 10
let test_crcl = (crcl (Point 1000 0) == 0)

let horizontally = fold (Point 0 0) (Point 1 0) crcl
let test_horizontally1 = horizontally (Point 0 0) == 1
let test_horizontally2 = horizontally (Point 0 1) == 2
let test_horizontally3 = horizontally (Point 0 (-1)) == 0

let vertically = fold (Point 0 0) (Point 0 1) crcl
let test_vertically1 = vertically (Point 0 0) == 1
let test_vertically2 = vertically (Point(-1) 0) == 2
let test_vertically2 = vertically (Point 1 0) == 0

let quarter = fold (Point 0 0) (Point 0 1) horizontally
let test_quarter1 = quarter (Point 0 0) == 1
let test_quarter2 = quarter (Point (-1) 1) == 4
let test_quarter3 = quarter (Point (-1) 0) == 2

let r = rectangle (Point 0 0) (Point 10 10)

let c = circle (Point 5 5) 5

let lines1 = NonEmpty (LineCoords (Point 0 0) (Point 10 10)) Empty


let lines2 = NonEmpty (LineCoords (Point 8 0) (Point 10 2))
        (NonEmpty (LineCoords (Point 6 0) (Point 10 4))
        (NonEmpty (LineCoords (Point 4 0) (Point 10 6))
        (NonEmpty (LineCoords (Point 2 0) (Point 10 8))
        (NonEmpty (LineCoords (Point 0 0) (Point 10 10))
        (NonEmpty (LineCoords (Point 0 2) (Point 8 10))
        (NonEmpty (LineCoords (Point 0 4) (Point 6 10))
        (NonEmpty (LineCoords (Point 0 6) (Point 4 10))
        (NonEmpty (LineCoords (Point 0 8) (Point 2 10))
        (Empty)))))))))


let mfr1 = multi_fold lines1 r
let mfr2 = multi_fold lines2 r
let mfc1 = multi_fold lines1 c


let test_mfr1_1 = mfr1 (Point 7 3) == 0
let _ = r (Point 1 1)
