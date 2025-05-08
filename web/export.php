<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $department = $_POST['department'] ?? '';
    $name = $_POST['name'] ?? '';

    if (!empty($department) && !empty($name)) {
        $file = 'data/participants.csv';
        $entry = "$department,$name\n";

        // Append the entry to the CSV file
        file_put_contents($file, $entry, FILE_APPEND | LOCK_EX);
        echo "<p>成功添加: 部门 - $department, 姓名 - $name</p>";
    } else {
        echo '<p style="color: red;">请填写所有字段！</p>';
    }
}
?>

<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>导出到CSV</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 400px;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        form {
            display: flex;
            flex-direction: column;
        }
        label {
            margin-bottom: 5px;
            color: #555;
        }
        input {
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: 16px;
        }
        button {
            padding: 10px;
            background-color: #007BFF;
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 16px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        p {
            text-align: center;
            color: #333;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>输入部门和姓名</h1>
        <form method="POST" action="export.php">
            <label for="department">部门:</label>
            <input type="text" id="department" name="department" required>

            <label for="name">姓名:</label>
            <input type="text" id="name" name="name" required>

            <button type="submit">提交</button>
        </form>
    </div>
</body>
</html>