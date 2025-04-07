from flask import Flask, request, render_template
app=Flask(__name__)
@app.route('/',methods=['GET','POST'])
def index():
    var=''
    if request.method=="POST"and "userweight" in request.form:
        weight=float(request.form.get("userweight"))
        height=float(request.form.get("userheight"))
        var=calc_bmi(weight,height)
    return render_template("bmi.html",var=var)
def calc_bmi(weight,height):
    return round((weight/((height/100)**2)),2)
if __name__ == "__main__":
    app.run(debug=True)