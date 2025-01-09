import matplotlib.pyplot as plt
import squarify
import seaborn as sb


def treemap_generate(values, labels, filename, top_n=None):
    sorted_data = sorted(zip(values, labels), reverse=True, key=lambda x: x[0])
    
    if top_n:
        sorted_data = sorted_data[:top_n]
    
    values, labels = zip(*sorted_data)

    labels = [f"{label}\n{value}" for label, value in zip(labels, values)]

    squarify.plot(
        sizes=values,
        label=labels,
        color = sb.color_palette("crest", len(values)),
        text_kwargs={'color':'white', 'fontsize':7,'weight':'bold'},
        ec = 'white'
        )
     
    plt.axis('off') 
    plt.savefig(filename, dpi=500, bbox_inches='tight', pad_inches=0)

    plt.clf()
    plt.close()
