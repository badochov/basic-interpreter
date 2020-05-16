let list_fold_left fun acc list ->
    |   Empty -> acc
    |   List head tail ->
            list_fold_left fun (fun acc head) tail
    end

let list_join list1 list2 =
    match list1 with
    |   List head tail ->
            List head (list_join tail list2)
    |   Empty -> list2
    end

let rectangle (x1, y1) (x2, y2) =
    fn (x, y) =
        if x1 <= x and x <= x2 and y1 <= y and y <= y2 then
            1
        else
            0

let circle (x1, y1) radius =
    fn (x, y) =
        if ((x1 - x) ^ 2 + (y1 - y) ^ 2) ^ 0.5 <= radius then
            1
        else
            0

let make_line (x1, y1) (x2, y2) = 
    let a = y1 - y2 in
    let b = x2 - x1 in
    let c = -y1 * b - x1 * a in
    a, b, c

let line_side (a, b, c) (x, y) =
    a * x + b * y + c

let denominator a b =
    (a ^ 2) + (b ^ 2)

let flip_x : int (a, b, c) (x, y) =
    let numerator = ((b ^ 2) - (a ^ 2)) * x - 2 * a * b * y  - 2 * a * c in
    numerator / denominator a b

let flip_y (a, b, c) (x, y) =
    let numerator = ((a ^ 2) - (b ^ 2)) * y - 2 * a * b * x  - 2 * b * c in
    numerator / denominator a b

let points_after_fold line point =
    let side = line_side line point in
    if side == 0 then
        [point]
    elif side < 0 then
        []
    else
        let x = flip_x line point in
        let y = flip_y line point in
        [point, (x, y)]

let fold point1 point2 paper =
    fn point =
        let count acc pnt = acc + paper pnt in
        let line = make_line point1 point2 in
        let points = points_after_fold line point in
        list_fold_left count 0 points


let multi_fold lines paper =
    let fold_helper acc (point1, point2) =
        fold point1 point2 acc
    in
    list_fold_left fold_helper paper lines


let test_rect1 = rectangle (0, 0) (2, 2) (2, 0) == 1
let test_rect2 = rectangle (0, 0) (2, 2) ((-1), 1) == 0

let test_circle1 = circle (0, 0) 2 (2, 0) == 1
let test_circle2 = circle (0, 0) 2 ((-1), 1) == 1
let test_circle3 = circle (0, 0) 2 ((-1), 2) == 0

let crcl = circle (0, 0) 10
let test_crcl = (crcl (1000, 0) == 0)

let horizontally = fold (0, 0) (1, 0) crcl
let test_horizontally1 = horizontally (0, 0) == 1
let test_horizontally2 = horizontally (0, 1) == 2
let test_horizontally3 = horizontally (0, (-1)) == 0

let vertically = fold (0, 0) (0, 1) crcl
let test_vertically1 = vertically (0, 0) == 1
let test_vertically2 = vertically ((-1), 0) == 2
let test_vertically2 = vertically (1, 0) == 0

let quarter = fold (0, 0) (0, 1) horizontally
let test_quarter1 = quarter (0, 0) == 1
let test_quarter2 = quarter ((-1), 1) == 4
let test_quarter3 = quarter ((-1), 0) == 2

let rctg = rectangle ((-10), (-10)) (10, 10)
let test_rctg = rctg (0, 0) == 1
let horizontally = fold (0, 0) (1, 0) rctg
let test_horizontally1 = horizontally (0, 0) == 1
let test_horizontally2 = horizontally (0, 1) == 2
let test_horizontally3 = horizontally (0, (-1)) == 0

let vertically = fold (0, 0) (0, 1) rctg
let test_vertically1 = vertically (0, 0) == 1
let test_vertically2 = vertically ((-1), 0) == 2
let test_vertically2 = vertically (1, 0) == 0

let quarter = fold (0, 0) (0, 1) horizontally
let test_quarter1 = quarter (0, 0) == 1
let test_quarter2 = quarter ((-1), 1) == 4
let test_quarter3 = quarter ((-1), 0) == 2

let r = rectangle (0, 0) (10, 10)

let c = circle (5, 5) 5

let lines1 = [
                ((0, 0), (10, 10)),
                ((5, 0), (10, 5)),
                ((10, 0), (0, 10)),
                ((2.5, 0), (2.5, 10)),
             ]


let lines2 = [
                ((8, 0), (10, 2)),
                ((6, 0), (10, 4)),
                ((4, 0), (10, 6)),
                ((2, 0), (10, 8)),
                ((0, 0), (10, 10)),
                ((0, 2), (8, 10)),
                ((0, 4), (6, 10)),
                ((0, 6), (4, 10)),
                ((0, 8), (2, 10)),
            ]


let mfr1 = multi_fold lines1 r
let mfr2 = multi_fold lines2 r
let mfc1 = multi_fold lines1 c


let test_mfr1_1 = mfr1 (7, 3) == 0
let test_mfr1_2 = mfr1 (5, 8) == 0
let test_mfr1_3 = mfr1 (3, 5) == 0
let test_mfr1_4 = mfr1 (5, 5) == 0
let test_mfr1_5 = mfr1 (0, 0) == 2
let test_mfr1_6 = mfr1 (0, 10) == 2
let test_mfr1_7 = mfr1 (2.5, 2.5) == 2
let test_mfr1_8 = mfr1 (2.5, 7.5) == 2
let test_mfr1_9 = mfr1 (2.5, 5) == 4
let test_mfr1_10 = mfr1 (0, 5) == 5
let test_mfr1_11 = mfr1 (1, 2) == 4
let test_mfr1_12 = mfr1 (1, 5) == 8
let test_mfr1_13 = mfr1 (1, 8) == 4

let test_mfc1_1 = mfc1 (7, 3) == 0
let test_mfc1_2 = mfc1 (5, 8) == 0
let test_mfc1_3 = mfc1 (3, 5) == 0
let test_mfc1_4 = mfc1 (5, 5) == 0
let test_mfc1_5 = mfc1 (2.5, 2.5) == 2
let test_mfc1_6 = mfc1 (2.5, 7.5) == 2
let test_mfc1_7 = mfc1 (2.5, 5) == 4
let test_mfc1_8 = mfc1 (0, 5) == 5
let test_mfc1_9 = mfc1 (1, 3) == 4
let test_mfc1_10 = mfc1 (1, 5) == 8
let test_mfc1_11 = mfc1 (1, 7) == 4

let test_mfr2_1 = mfr2 ((-4), 6) == 2
let test_mfr2_2 = mfr2 ((-3), 5) == 1
let test_mfr2_3 = mfr2 ((-3), 7) == 2
let test_mfr2_4 = mfr2 ((-2), 6) == 3
let test_mfr2_5 = mfr2 ((-2.5), 6.5) == 4
let test_mfr2_6 = mfr2 ((-2), 8) == 4
let test_mfr2_7 = mfr2 ((-1), 7) == 3
let test_mfr2_8 = mfr2 ((-1.5), 7.5) == 6
let test_mfr2_9 = mfr2 (0, 8) == 5
let test_mfr2_10 = mfr2 ((-1), 9) == 4
let test_mfr2_11 = mfr2 ((-0.5), 8.5) == 8
let test_mfr2_12 = mfr2 (0, 10) == 6
let test_mfr2_13 = mfr2 (1, 9) == 5
let test_mfr2_14 = mfr2 (0.5, 9.5) == 10


# Version with outputting points

let rectangle_point (x1, y1) (x2, y2) =
    fn (x, y) =
        if x1 <= x and x <= x2 and y1 <= y and y <= y2 then
            [point]
        else
            []
        

let circle_point (x1, y1) radius =
    fn (x, y) = 
        if ((x1 - x) ^ 2 + (y1 - y) ^ 2) ^ 0.5 <= radius then
            [point]
        else
            []

let fold_points point1 point2 paper =
    fn point =
        let count acc pnt = list_join acc (paper pnt) in
        let line = make_line point1 point2 in
        let points = points_after_fold line point in
        list_fold_left count [] points

let multi_fold_points lines paper =
    let fold_helper acc (point1, point2) =
        fold_points point1 point2 acc
    in
    list_fold_left fold_helper paper lines


let r_p = rectangle_point (0, 0) (10, 10)
let crclp = circle_point (0, 0) 10
let test_crclp = crclp (1000, 0)

let horizontallyp = fold_points (0, 0) (1, 0) crclp
let test_horizontally1p = horizontallyp (0, 0)
let test_horizontally2p = horizontallyp (0, 1)
let test_horizontally3p = horizontallyp (0, (-1))

let verticallyp = fold_points (0, 0) (0, 1) crclp
let test_vertically1p = verticallyp (0, 0)
let test_vertically2p = verticallyp ((-1), 0)
let test_vertically3p = verticallyp (1, 0)

let quarterp = fold_points (0, 0) (0, 1) horizontallyp
let test_quarter1p = quarterp (0, 0)
let test_quarter2p = quarterp ((-1), 1)
let test_quarter3p = quarterp ((-1), 0)