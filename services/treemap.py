import matplotlib.pyplot as plt
import squarify
import seaborn as sb


def treemap_generate(values, labels, filename):
    for i in range(len(labels)):
        labels[i] = f"{labels[i]}\n{values[i]}"

    squarify.plot(
        sizes=values,
        label=labels,
        color = sb.color_palette("crest", len(values)),
        text_kwargs={'color':'white', 'fontsize':10,'weight':'bold'},
        ec = 'white'
        )
     
    plt.axis('off') 
    plt.savefig(filename, dpi=500, bbox_inches='tight', pad_inches=0)
