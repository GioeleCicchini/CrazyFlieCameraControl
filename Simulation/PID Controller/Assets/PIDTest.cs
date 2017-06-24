using UnityEngine;
using System.Collections;

public class PIDTest : MonoBehaviour
{


    public float speed;
    public Transform actual;
    public Transform setpoint;
    public float g;

    public PID rollPID;
    public PID pitchPID;
    public PID heightPID;
    public PID yawPID;

    public SimpleKalmanFilter kalmanRoll;
    public SimpleKalmanFilter kalmanPitch;

    public Rigidbody rb;


    void Start()
    {
        rb = actual.GetComponent<Rigidbody>();
  
    }


    void Update()
    {


        var heading = actual.rotation.y;

        var rollPIDvalue = rollPID.Update(setpoint.position.x, actual.position.x, Time.deltaTime);
        var pitchPIDvalue = pitchPID.Update(setpoint.position.z, actual.position.z, Time.deltaTime);
        var heightPIDvalue = heightPID.Update(setpoint.position.y, actual.position.y, Time.deltaTime);
        var yawPIDvalue = yawPID.Update(0, heading, Time.deltaTime);


        var desiredRoll = -rollPIDvalue * Mathf.Cos((heading * Mathf.PI) / 180) + pitchPIDvalue * Mathf.Sin((heading * Mathf.PI) / 180) * (1 / g);
        var desiredPitch = pitchPIDvalue * Mathf.Cos((heading * Mathf.PI) / 180) - rollPIDvalue * Mathf.Sin((heading * Mathf.PI) / 180) * (1 / g);
        var desiredThrottle = (heightPIDvalue + g) * rb.mass / Mathf.Cos(actual.rotation.x) * Mathf.Cos(actual.rotation.y);
        var desiredYaw = (yawPIDvalue * 0.1f);

       desiredRoll = (float)kalmanRoll.KalmanUpdate(desiredRoll);
        desiredPitch = (float)kalmanPitch.KalmanUpdate(desiredPitch);



        setpoint.Translate(Input.GetAxis("Horizontal") * Time.deltaTime * speed, 0, 0);


        actual.transform.rotation = Quaternion.Euler(desiredPitch, desiredYaw, desiredRoll);

        rb.AddRelativeForce(Vector3.up * desiredThrottle);


    }
}
