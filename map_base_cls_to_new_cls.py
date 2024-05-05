from pathlib import Path

labels_dir = Path("dataset\\labels")

valid_cls = 0, 1, 2, 3, 4, 11, 80, 81, 82, 83, 84, 11

skip = False

for label in labels_dir.glob("*.txt"):
    if label.name == "classes.txt":
        continue

    with open(label, "r+") as f:
        lines = [line for line in f.read().split("\n") if line]
        new_lines: list[str] = []

        for line in lines:
            nums = line.split(" ")
            cls = int(nums[0])

            if cls not in valid_cls:
                print(label, line)
                skip = True
                break
            elif cls == 1:
                nums[0] = "1"
            elif cls == 2:
                nums[0] = "2"
            elif cls == 3:
                nums[0] = "3"
            elif cls == 4:
                nums[0] = "4"
            elif cls == 11:
                nums[0] = "0"
            elif cls == 80:
                nums[0] = "0"
            elif cls == 81:
                nums[0] = "1"
            elif cls == 82:
                nums[0] = "2"
            elif cls == 83:
                nums[0] = "3"
            elif cls == 84:
                nums[0] = "4"
            elif cls == 11:
                nums[0] = "1"

            new_line = " ".join(nums)
            new_line_w_nl = f"{new_line}\n"
            new_lines.append(new_line_w_nl)

        if skip:
            skip = False
            continue

        f.seek(0)
        f.truncate()
        f.writelines(new_lines)
