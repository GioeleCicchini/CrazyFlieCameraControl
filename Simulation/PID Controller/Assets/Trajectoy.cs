using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Trajectoy : MonoBehaviour {

	// Use this for initialization
	void Start () {
		
	}

    float angle = 0;
    public float speed; 
    float radius = 5;

    public bool active;
    void Update()
    {
        if (active)
        {
            angle += speed * Time.deltaTime; //if you want to switch direction, use -= instead of +=
            radius -= 0.0005f; 
            transform.position = new Vector3(200 + Mathf.Cos(angle) * radius, transform.position.y + 0.005f, 200 + Mathf.Sin(angle) * radius);
        }

      


    }
    // Update is called once per frame

}
