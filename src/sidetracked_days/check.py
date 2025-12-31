


threshold = 0.8 # %

def cmpr(model, cpr):

    if not model or not cpr:
        return False

    if len(model) != len(cpr):
        return False

    for i in range(len(model)):

        x_diff = model[i][0] - cpr[i][0]
        y_diff = model[i][1] - cpr[i][1]

        if x_diff > threshold or y_diff > threshold:
            return False

    return True

        # x_mid = (model[i][0] + cpr[i][0]) / 2
        # y_mid = (model[i][1] + cpr[i][1]) / 2

        
