from pathlib import Path

import ulid
from config.coordinate import CORRECT_TRAJECTORY_COORDINATES1

# バッチ用のリスト
estimated_positions_values = []
correct_positions_values = []

trajectory_id = "01JET1DV4WJ2EP78B8HAKK5SP0"
walking_information_id = "01JHC3VK41160ZSFWJDT24T1Z6"

for coord in CORRECT_TRAJECTORY_COORDINATES1:
    x, y, _, direction, _ = coord

    # 推定位置データ
    estimated_position_id = str(ulid.new())
    estimated_positions_values.append(
        f"('{estimated_position_id}', {x}, {y}, TRUE, {direction}, '{trajectory_id}', '{walking_information_id}')"
    )

    # 正解位置データ
    correct_position_id = str(ulid.new())
    correct_positions_values.append(f"('{correct_position_id}', {x}, {y}, {direction}, '{trajectory_id}')")

# SQL文を組み立て
estimated_positions_sql = (
    "INSERT INTO estimated_positions (id, x, y, is_converged, direction, trajectory_id, walking_information_id) VALUES\n"
    + ",\n".join(estimated_positions_values)
    + ";"
)

correct_positions_sql = (
    "INSERT INTO correct_positions (id, x, y, direction, trajectory_id) VALUES\n" + ",\n".join(correct_positions_values) + ";"
)

# 出力
output_sql = estimated_positions_sql + "\n\n" + correct_positions_sql
print(output_sql)

# ファイルに書き込み
with Path("insert_position.sql").open("w") as f:
    f.write(output_sql)
