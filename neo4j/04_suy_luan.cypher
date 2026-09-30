// Tu giac
MATCH
    (q:TuGiac),
    (h:LoaiHinh {id: "TU_GIAC"})
WHERE
    q.hop_le = true
MERGE (q)-[:THUOC_LOAI]->(h);


// Hinh thang
MATCH
    (q:TuGiac),
    (h:LoaiHinh {id: "HINH_THANG"})
WHERE
    q.hop_le = true
    AND q.so_cap_song_song >= 1
MERGE (q)-[:THUOC_LOAI]->(h);


// Hinh binh hanh
MATCH
    (q:TuGiac),
    (h:LoaiHinh {id: "HINH_BINH_HANH"})
WHERE
    q.hop_le = true
    AND q.so_cap_song_song = 2
MERGE (q)-[:THUOC_LOAI]->(h);


// Hinh chu nhat
MATCH
    (q:TuGiac),
    (h:LoaiHinh {id: "HINH_CHU_NHAT"})
WHERE
    q.hop_le = true
    AND q.so_cap_song_song = 2
    AND q.so_goc_vuong >= 1
MERGE (q)-[:THUOC_LOAI]->(h);


// Hinh thoi
MATCH
    (q:TuGiac),
    (h:LoaiHinh {id: "HINH_THOI"})
WHERE
    q.hop_le = true
    AND q.bon_canh_bang_nhau = true
MERGE (q)-[:THUOC_LOAI]->(h);


// Hinh vuong
MATCH
    (q:TuGiac),
    (h:LoaiHinh {id: "HINH_VUONG"})
WHERE
    q.hop_le = true
    AND q.so_cap_song_song = 2
    AND q.so_goc_vuong >= 1
    AND q.bon_canh_bang_nhau = true
MERGE (q)-[:THUOC_LOAI]->(h);


// Hinh thang can
MATCH
    (q:TuGiac)-[:CO_CANH]->(ab:DoanThang {ten: "AB"}),
    (q)-[:CO_CANH]->(bc:DoanThang {ten: "BC"}),
    (q)-[:CO_CANH]->(cd:DoanThang {ten: "CD"}),
    (q)-[:CO_CANH]->(da:DoanThang {ten: "DA"}),
    (h:LoaiHinh {id: "HINH_THANG_CAN"})

WHERE
    q.hop_le = true
    AND q.so_cap_song_song = 1
    AND (
        (
            EXISTS {
                MATCH (ab)-[:SONG_SONG_VOI]-(cd)
            }
            AND EXISTS {
                MATCH (bc)-[:BANG_NHAU_VOI]-(da)
            }
        )
        OR
        (
            EXISTS {
                MATCH (bc)-[:SONG_SONG_VOI]-(da)
            }
            AND EXISTS {
                MATCH (ab)-[:BANG_NHAU_VOI]-(cd)
            }
        )
    )

MERGE (q)-[:THUOC_LOAI]->(h);


// Hinh thang vuong
MATCH
    (q:TuGiac),
    (h:LoaiHinh {id: "HINH_THANG_VUONG"})

WHERE
    q.hop_le = true
    AND q.so_cap_song_song = 1
    AND q.so_goc_vuong >= 2

MERGE (q)-[:THUOC_LOAI]->(h);