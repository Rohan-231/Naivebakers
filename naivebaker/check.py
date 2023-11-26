import requests
# https://api.edamam.com/search?q=${finalSearchValue}&app_id=7aa516a5&app_key=dc836a223fb788b11ae390504d9e97ce&from=0&to=${limit}

response = requests.get('https://api.edamam.com/search?q=potato&app_id=7aa516a5&app_key=dc836a223fb788b11ae390504d9e97ce&from=0&to=7')
print(response.status_code)
data = (response.json())
# print(data)
# const nik1 = data.hits
nik2 = data['hits']
# print(nik2)
# print(nik2)
# //console.log(nik2.recipe.mealType[0])
# displayRecipes(data.hits);
html = '' 
for hit in nik2:
    name = hit['recipe']['label']
    image = hit['recipe']['image']
    cuisineType = hit['recipe']['cuisineType']
    mealType = hit['recipe']['mealType']
    url = hit['recipe']['url']
    print(url)
    # html+= '''
    # <div class="ncard col-lg-3 col-md-4 col-sm-6 col-xs-12 border my-5 m-1">
    #     {% csrf_token %}
    #     <figure class="figure">
    #         <img src="${recipe.recipe.image}" class="image img-fluid rounded-5" alt="${recipe.recipe.label}">
    #     </figure>

    #     <div class="second row mt-2">
    #         <div class="chef col-lg-6 d-flex justify-content-start">
    #             <div class="chefname">
    #                 <div>-By abcdefghijk</div>
    #                 <div class="line"></div>
    #                 <div class="text-end">LA</div>
    #             </div>
    #         </div>

    #         <div class="recipe col-lg-6 col-sm-12 d-flex justify-content-lg-end">
    #             <div class="chefname">
    #                 <div class="row">
    #                     <span class="fs-10 fw-bolder recipename">
    #                         ${recipe.recipe.label}
    #                     </span>
    #                 </div>
    #                 <div class="fs-6 fw-bolder">
    #                     <span style="color: blue;">4.5</span>
    #                     <span style="color: orange;">rating</span>
    #                 </div>
    #             </div>
    #         </div>
    #     </div>

    #     <div class="third row d-flex justify-content-between mt-2">
    #         <div class="col-lg-6 col-sm-12 justify-content-lg-start">
    #             ${recipe.recipe.cuisineType}, ${recipe.recipe.mealType}
    #         </div>
    #         <div class="col-lg-6 col-sm-12 justify-content-lg-end text-end">
    #             20 min
    #         </div>
    #     </div>

    #     <div class="line"></div>

    #     <br>

    #     <div class="fourth d-flex justify-content-between">
    #         <div class="lss like likeone mx-auto">
    #             <button class="btn btn-transparent btn-sm " name="like" id="like">
    #                 <i class="fa-solid fa-heart"></i>
    #                 Like
    #             </button>
    #         </div>
    #         <div class="lss share mx-auto">
    #             <button class="btn btn-transparent btn-sm" name="share" id="share">
    #                 <i class="fa-sharp fa-solid fa-share-nodes"></i>
    #                 Share
    #             </button>
    #         </div>
    #         <div class="lss save mx-auto">
    #             <button class="btn btn-transparent btn-sm save" name="save" id="save">
    #                 <i class="fa-solid fa-floppy-disk"></i>
    #                 Save
    #             </button>
    #         </div>
    #     </div>

    #     <div class="fifth cook d-flex justify-content-center mx-auto mt-3 mb-1">
    #         <button class="btn btn-transparent btn-sm" onclick="window.open('${recipe.recipe.url}', '_blank')"; name="cook" id="cook">
    #             <div class="fs-4">
    #                 cook
    #             </div>
    #         </button>
    #     </div>
    # </div>'''

# Now you can use the 'html' string as needed in your Python code.
