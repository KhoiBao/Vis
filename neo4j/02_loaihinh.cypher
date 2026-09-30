CREATE
    (:LoaiHinh {
        id: "TU_GIAC",
        ten: "Tu giac"
    }),

    (:LoaiHinh {
        id: "HINH_THANG",
        ten: "Hinh thang"
    }),

    (:LoaiHinh {
        id: "HINH_THANG_CAN",
        ten: "Hinh thang can"
    }),

    (:LoaiHinh {
        id: "HINH_THANG_VUONG",
        ten: "Hinh thang vuong"
    }),

    (:LoaiHinh {
        id: "HINH_BINH_HANH",
        ten: "Hinh binh hanh"
    }),

    (:LoaiHinh {
        id: "HINH_CHU_NHAT",
        ten: "Hinh chu nhat"
    }),

    (:LoaiHinh {
        id: "HINH_THOI",
        ten: "Hinh thoi"
    }),

    (:LoaiHinh {
        id: "HINH_VUONG",
        ten: "Hinh vuong"
    });

MATCH
    (tuGiac:LoaiHinh {id: "TU_GIAC"}),
    (hinhThang:LoaiHinh {id: "HINH_THANG"}),
    (hinhThangCan:LoaiHinh {id: "HINH_THANG_CAN"}),
    (hinhThangVuong:LoaiHinh {id: "HINH_THANG_VUONG"}),
    (hinhBinhHanh:LoaiHinh {id: "HINH_BINH_HANH"}),
    (hinhChuNhat:LoaiHinh {id: "HINH_CHU_NHAT"}),
    (hinhThoi:LoaiHinh {id: "HINH_THOI"}),
    (hinhVuong:LoaiHinh {id: "HINH_VUONG"})

CREATE
    (hinhThang)-[:LA_MOT_LOAI_CUA]->(tuGiac),
    (hinhThangCan)-[:LA_MOT_LOAI_CUA]->(hinhThang),
    (hinhThangVuong)-[:LA_MOT_LOAI_CUA]->(hinhThang),

    (hinhBinhHanh)-[:LA_MOT_LOAI_CUA]->(tuGiac),
    (hinhChuNhat)-[:LA_MOT_LOAI_CUA]->(hinhBinhHanh),
    (hinhThoi)-[:LA_MOT_LOAI_CUA]->(hinhBinhHanh),

    (hinhVuong)-[:LA_MOT_LOAI_CUA]->(hinhChuNhat),
    (hinhVuong)-[:LA_MOT_LOAI_CUA]->(hinhThoi);