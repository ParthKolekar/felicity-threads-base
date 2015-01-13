<?php
	$conn = mysqli_connect('localhost' , 'root' , 'saphira' , 'felicity_threads_base');
	$query = $conn->prepare("SELECT user_nick , user_score FROM base_user ORDER BY user_score DESC , user_total_time ASC");
	$query->execute();

	$index = 1;

	$query->bind_result($user_nick,$user_score);
	$scores = array();
	while ($query->fetch()) {
		$score = array(
			'index' => $index,
	        'user_nick' => $user_nick,
	        'score' => $user_score
	    );  
		array_push($scores, $score);
		$index = $index + 1;
	}
	$query->close();

	echo json_encode($scores);

	$conn->close();
?>
