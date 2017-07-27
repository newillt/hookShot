<?php
$servername = "localhost";
$username = "root";
$password = "20150919taylor";
$dbname = "database1";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 


   
	$sql = "SELECT * FROM teamData;"
	echo $sql
	$result=$conn->query($sql);

echo '<head><link rel="stylesheet" href="style.css" type="text/css" /></head><div class="datagrid"><table>
<thead><tr><th>Team Name</th><th>Game Date</th><th>Points Allowed</th><th>Total Points Allowed</th></tr></thead>
<tfoot><tr><td colspan="4"><div id="paging"><ul><li><a href="#"><span>Previous</span></a></li><li><a href="#" class="active"><span>1</span></a></li><li><a href="#"><span>2</span></a></li><li><a href="#"><span>3</span></a></li><li><a href="#"><span>4</span></a></li><li><a href="#"><span>5</span></a></li><li><a href="#"><span>Next</span></a></li></ul></div></tr></tfoot>
<tbody>';


if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
        echo "<tr valign='top'>";
	echo "<td>" . $row["teamName"]. "</td>";
	echo "<td>" . $row["gameDate"]. "</td>";
	echo "<td>" . $row["pointsAllowed"]. "</td>";
	echo "<td>" . $row["totalPointsAllowed"]."</td>";
	echo "</td>";
    }
} else {
    echo "0 results";
}
echo '</tbody></table></div></html>';
$conn->close();


?>
