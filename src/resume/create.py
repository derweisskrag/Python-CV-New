from resume.resume import Resume

def create_cv(data, output_name):
    print("Hello, Python!")
    my_cv = Resume(data, output_name)
    my_cv.generate_simple_cv()


