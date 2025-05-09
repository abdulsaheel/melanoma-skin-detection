from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image
import numpy as np
import skin_cancer_detection as SCD
import io

app = FastAPI()

templates = Jinja2Templates(directory="templates")

info = {
    0: "Actinic keratosis also known as solar keratosis or senile keratosis are names given to intraepithelial keratinocyte dysplasia. As such they are a pre-malignant lesion or in situ squamous cell carcinomas and thus a malignant lesion.",
    1: "Basal cell carcinoma is a type of skin cancer. Basal cell carcinoma begins in the basal cells—a type of cell within the skin that produces new skin cells as old ones die off. Basal cell carcinoma often appears as a slightly transparent bump on the skin, though it can take other forms. Basal cell carcinoma occurs most often on areas of the skin that are exposed to the sun, such as your head and neck.",
    2: "Benign lichenoid keratosis (BLK) usually presents as a solitary lesion that occurs predominantly on the trunk and upper extremities in middle-aged women. The pathogenesis of BLK is unclear; however, it has been suggested that BLK may be associated with the inflammatory stage of regressing solar lentigo (SL).",
    3: "Dermatofibromas are small, noncancerous (benign) skin growths that can develop anywhere on the body but most often appear on the lower legs, upper arms or upper back. These nodules are common in adults but are rare in children. They can be pink, gray, red or brown in color and may change color over the years. They are firm and often feel like a stone under the skin.",
    4: "A melanocytic nevus (also known as nevocytic nevus, nevus-cell nevus and commonly as a mole) is a type of melanocytic tumor that contains nevus cells. Some sources equate the term mole with 'melanocytic nevus', but there are also sources that equate the term mole with any nevus form.",
    5: "Pyogenic granulomas are skin growths that are small, round, and usually bloody red in color. They tend to bleed because they contain a large number of blood vessels. They're also known as lobular capillary hemangioma or granuloma telangiectaticum.",
    6: "Melanoma, the most serious type of skin cancer, develops in the cells (melanocytes) that produce melanin—the pigment that gives your skin its color. Melanoma can also form in your eyes and, rarely, inside your body, such as in your nose or throat. The exact cause of all melanomas isn't clear, but exposure to ultraviolet (UV) radiation from sunlight or tanning lamps and beds increases your risk of developing melanoma."
}

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict")
async def predict(request: Request):
    image_data = await request.body()
    input_image = Image.open(io.BytesIO(image_data)).resize((28, 28))
    img_array = np.array(input_image).reshape(-1, 28, 28, 3)

    prediction = SCD.model.predict(img_array)
    predicted_class_index = np.argmax(prediction, axis=1)[0]
    predicted_class = SCD.classes[predicted_class_index]
    detailed_info = info[predicted_class_index]

    response = {
        "predicted_class": predicted_class,
        "detailed_information": detailed_info,
        "probability": float(np.max(prediction))
    }

    return JSONResponse(content=response)
