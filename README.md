# About Selfie2Pro
## A professional image generator.
**Need a professional photo for job applications, ID's or personal document
but don't have the resources?**
**We're here to help!**

With a lot of important documents, there's also a need for a photo that suits
the occassion. A good professional photo requires a matching location and 
outfit, not to mention someone who can take the photo, all of which require time
and money. For those who lack the resources to get a professional photo done,
this tool is the best help for you!

With just a single selfie and a few minutes of your time, Selfie2Proshot will 
generate an optimized photo with based on your selfie that rivals 
professional photos.

*All it takes is 3 simple steps!* Go to the site, upload a selfie and 
get your photo!

### How to run
First, we need to install all the libraries on cloud9 based on the given instructions and then go to the `selfie2proshot/pipeline` directory and then run the following command:
```
cd selfie2proshot/pipeline
streamlit run app.py --server.port 8080 --server.enableXsrfProtection=false
```

### Convenient features
- Automatic background changer. No prompts or questions asked.
- Automatic image resizer. No editing/resizing of image required. The program 
will format the photo to match the AI model's image requirements.
- Optimized positioning. Posture and position of person will be automatically generated.
- Photo editing. Image will be touched up and editied just like a professional 
photo.
- Simple and straightforward UI. 1 simple page for 1 amazing solution.


### How it works:
- The site takes in an upload from the user.
- Image is then scaled and resized.
- Photo is passed through into the (Insert AI model) model, with an optimized
prompt to generate the new image.
- Ouptut generation and then output is displayed.

### Next Steps: 
With the same mission of minimzing the cost of taking professional photos, our 
plans for the future of the project includes an automated clothes changer, 
better posture and expression reccomendations, better editing techniques, and most  improved generation consistency.



## Resources
- Amazon Titan
- Streamlit
- Amazon Bedrock
  
