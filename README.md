# Harry-Potters-Cloak
Build Harry Potter's Cloak using Open CV and Numpy in Pyton

This project uses two popular python libraries - Open CV and Numpy to recreate the effect of Harry Potter's Cloak of invisibility.
Using live feed from the webcam, first the user must run the code to take a picture of the background without being in it. This picture without the user, would act as the reference picture to show what is behind the person, hence recreating the invisibility effect.

Secondly, the person can use the various sliders present above to adjust the HSV values to the color of the object that will be acting as the cloak. This can be verified by displaying the mask and mask_inv properties along with the original webcam view and final webcam views.

The final result is achieved using bitwise operators with the masks produced using the above step.




https://user-images.githubusercontent.com/59104356/131535324-61dd4549-5c4c-4fa8-9fdd-956527380120.mov


