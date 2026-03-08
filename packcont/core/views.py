import math

from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages

from . import constants as const
from .utils import items_str_to_list, Containers, containers_to_table

# Create your views here.

class Index(View):
    def dispatch(self, request, *args, **kwargs):
        try:
            variant = kwargs.get('slug', '').upper()
            if variant not in const.VARIANTS.keys():
                messages.info(request, "Невідомий варіант. Будь ласка, виберіть існуючий варіант.")
                return redirect('start-page')
        except Exception as e:
            messages.info(request, "Щось пішло не так. Йойки")
            return redirect('start-page')
        return super().dispatch(request, *args, **kwargs)
    def get(self, request, *args, **kwargs):
        v = kwargs.get('slug', '')
        v = v.upper()
        context = {         
            'capacity': const.CAPACITY,
            
            'items1': const.VARIANTS[v]['ITEMS_1_RAW'],
            'items2': const.VARIANTS[v]['ITEMS_2_RAW'],
            'items3': const.VARIANTS[v]['ITEMS_3_RAW'],
        }
        return render(request, 'core/index.html', context)
    
    def post(self, request, *args, **kwargs):
        variant = kwargs.get('slug', '').upper()
        items1_raw = request.POST.get('items1')
        items1_raw = items1_raw if items1_raw else const.VARIANTS[variant]['ITEMS_1_RAW']
        
        items2_raw = request.POST.get('items2')
        items2_raw = items2_raw if items2_raw else const.VARIANTS[variant]['ITEMS_2_RAW']
        
        items3_raw = request.POST.get('items3')
        items3_raw = items3_raw if items3_raw else const.VARIANTS[variant]['ITEMS_3_RAW']
        
        capacity = request.POST.get('capacity')
        capacity = int(capacity) if capacity else const.CAPACITY
        
        
        good1, items1 = items_str_to_list(items1_raw, 1)
        good2, items2 = items_str_to_list(items2_raw, 2)
        good3, items3 = items_str_to_list(items3_raw, 3)
        
        context = {         
            'capacity': capacity,
            
            'items1': const.VARIANTS[variant]['ITEMS_1_RAW'],
            'items2': const.VARIANTS[variant]['ITEMS_2_RAW'],
            'items3': const.VARIANTS[variant]['ITEMS_3_RAW'],
        }
        
        if not good1:
            messages.info(request, items1)
            return render(request, 'core/index.html', context=context)
        if not good2:
            messages.info(request, items2)
            return render(request, 'core/index.html', context=context)
        if not good3:
            messages.info(request, items3)
            return render(request, 'core/index.html', context=context)
        
        if capacity < max(items1):
            messages.info(request, f"Всі предмети 1 повинні бути меншими або рівними за ємність контейнера. Замініть елемент {max(items1)} на число, що не перевищує {capacity}.")
            return render(request, 'core/index.html', context=context)
        
        if capacity < max(items2):
            messages.info(request, f"Всі предмети 2 повинні быть меньшими или равными за емкость контейнера. Замените элемент {max(items2)} на число, что не превышает {capacity}.")
            return render(request, 'core/index.html', context=context)
        
        if capacity < max(items3):
            messages.info(request, f"Всі предмети 3 повинні быть меньшими или равными за емкость контейнера. Замените элемент {max(items3)} на число, что не превышает {capacity}.")
            return render(request, 'core/index.html', context=context)
        
        #!for items 1
        items1_container = Containers(capacity=capacity)
        items1_container.add_item(items1)
        
        nfa1 = items1_container.NFA()
        ffa1 = items1_container.FFA()
        wfa1 = items1_container.WFA()
        bfa1 = items1_container.BFA()

        nfa1_table, nfa1_rows, nfa1_cols = containers_to_table(nfa1)
        ffa1_table, ffa1_rows, ffa1_cols = containers_to_table(ffa1)
        wfa1_table, wfa1_rows, wfa1_cols = containers_to_table(wfa1)
        bfa1_table, bfa1_rows, bfa1_cols = containers_to_table(bfa1)
        
        algorithm_complexity_nfa1 = items1_container.algorithm_complexity_nfa
        algorithm_complexity_ffa1 = items1_container.algorithm_complexity_ffa
        algorithm_complexity_wfa1 = items1_container.algorithm_complexity_wfa
        algorithm_complexity_bfa1 = items1_container.algorithm_complexity_bfa
        
        nfa1s = items1_container.NFA(sort=True)
        ffa1s = items1_container.FFA(sort=True)
        wfa1s = items1_container.WFA(sort=True)
        bfa1s = items1_container.BFA(sort=True)
        
        nfa1s_table, nfa1s_rows, nfa1s_cols = containers_to_table(nfa1s)
        ffa1s_table, ffa1s_rows, ffa1s_cols = containers_to_table(ffa1s)
        wfa1s_table, wfa1s_rows, wfa1s_cols = containers_to_table(wfa1s)
        bfa1s_table, bfa1s_rows, bfa1s_cols = containers_to_table(bfa1s)
        
        algorithm_complexity_nfa1s = items1_container.algorithm_complexity_nfa
        algorithm_complexity_ffa1s = items1_container.algorithm_complexity_ffa
        algorithm_complexity_wfa1s = items1_container.algorithm_complexity_wfa
        algorithm_complexity_bfa1s = items1_container.algorithm_complexity_bfa
                                                                  
        context.update({
            'nfa1': nfa1_table, 'nfa1_rows': nfa1_rows, 'nfa1_cols': nfa1_cols,
            'ffa1': ffa1_table, 'ffa1_rows': ffa1_rows, 'ffa1_cols': ffa1_cols,
            'wfa1': wfa1_table, 'wfa1_rows': wfa1_rows, 'wfa1_cols': wfa1_cols,
            'bfa1': bfa1_table, 'bfa1_rows': bfa1_rows, 'bfa1_cols': bfa1_cols,
            
            'nfa1s': nfa1s_table, 'nfa1s_rows': nfa1s_rows, 'nfa1s_cols': nfa1s_cols,
            'ffa1s': ffa1s_table, 'ffa1s_rows': ffa1s_rows, 'ffa1s_cols': ffa1s_cols,
            'wfa1s': wfa1s_table, 'wfa1s_rows': wfa1s_rows, 'wfa1s_cols': wfa1s_cols,
            'bfa1s': bfa1s_table, 'bfa1s_rows': bfa1s_rows, 'bfa1s_cols': bfa1s_cols,
            
            'algorithm_complexity_nfa1': algorithm_complexity_nfa1,
            'algorithm_complexity_ffa1': algorithm_complexity_ffa1,
            'algorithm_complexity_wfa1': algorithm_complexity_wfa1,
            'algorithm_complexity_bfa1': algorithm_complexity_bfa1,
            
            'algorithm_complexity_nfa1s': algorithm_complexity_nfa1s,
            'algorithm_complexity_ffa1s': algorithm_complexity_ffa1s,
            'algorithm_complexity_wfa1s': algorithm_complexity_wfa1s,
            'algorithm_complexity_bfa1s': algorithm_complexity_bfa1s,
        })
        
        #!for items 2
        items2_container = Containers(capacity=capacity)
        items2_container.add_item(items2)
        
        nfa2 = items2_container.NFA()
        ffa2 = items2_container.FFA()
        wfa2 = items2_container.WFA()
        bfa2 = items2_container.BFA()

        nfa2_table, nfa2_rows, nfa2_cols = containers_to_table(nfa2)
        ffa2_table, ffa2_rows, ffa2_cols = containers_to_table(ffa2)
        wfa2_table, wfa2_rows, wfa2_cols = containers_to_table(wfa2)
        bfa2_table, bfa2_rows, bfa2_cols = containers_to_table(bfa2)
        
        algorithm_complexity_nfa2 = items2_container.algorithm_complexity_nfa
        algorithm_complexity_ffa2 = items2_container.algorithm_complexity_ffa
        algorithm_complexity_wfa2 = items2_container.algorithm_complexity_wfa
        algorithm_complexity_bfa2 = items2_container.algorithm_complexity_bfa

        nfa2s = items2_container.NFA(sort=True)
        ffa2s = items2_container.FFA(sort=True)
        wfa2s = items2_container.WFA(sort=True)
        bfa2s = items2_container.BFA(sort=True)
        
        nfa2s_table, nfa2s_rows, nfa2s_cols = containers_to_table(nfa2s)
        ffa2s_table, ffa2s_rows, ffa2s_cols = containers_to_table(ffa2s)
        wfa2s_table, wfa2s_rows, wfa2s_cols = containers_to_table(wfa2s)
        bfa2s_table, bfa2s_rows, bfa2s_cols = containers_to_table(bfa2s)
        
        algorithm_complexity_nfa2s = items2_container.algorithm_complexity_nfa
        algorithm_complexity_ffa2s = items2_container.algorithm_complexity_ffa
        algorithm_complexity_wfa2s = items2_container.algorithm_complexity_wfa
        algorithm_complexity_bfa2s = items2_container.algorithm_complexity_bfa

        context.update({
            'nfa2': nfa2_table, 'nfa2_rows': nfa2_rows, 'nfa2_cols': nfa2_cols,
            'ffa2': ffa2_table, 'ffa2_rows': ffa2_rows, 'ffa2_cols': ffa2_cols,
            'wfa2': wfa2_table, 'wfa2_rows': wfa2_rows, 'wfa2_cols': wfa2_cols,
            'bfa2': bfa2_table, 'bfa2_rows': bfa2_rows, 'bfa2_cols': bfa2_cols,
            
            'nfa2s': nfa2s_table, 'nfa2s_rows': nfa2s_rows, 'nfa2s_cols': nfa2s_cols,
            'ffa2s': ffa2s_table, 'ffa2s_rows': ffa2s_rows, 'ffa2s_cols': ffa2s_cols,
            'wfa2s': wfa2s_table, 'wfa2s_rows': wfa2s_rows, 'wfa2s_cols': wfa2s_cols,
            'bfa2s': bfa2s_table, 'bfa2s_rows': bfa2s_rows, 'bfa2s_cols': bfa2s_cols,
            
            'algorithm_complexity_nfa2': algorithm_complexity_nfa2,
            'algorithm_complexity_ffa2': algorithm_complexity_ffa2,
            'algorithm_complexity_wfa2': algorithm_complexity_wfa2,
            'algorithm_complexity_bfa2': algorithm_complexity_bfa2,
            
            'algorithm_complexity_nfa2s': algorithm_complexity_nfa2s,
            'algorithm_complexity_ffa2s': algorithm_complexity_ffa2s,
            'algorithm_complexity_wfa2s': algorithm_complexity_wfa2s,
            'algorithm_complexity_bfa2s': algorithm_complexity_bfa2s,
        })
        
        #!for items 3
        items3_container = Containers(capacity=capacity)
        items3_container.add_item(items3)
        
        nfa3 = items3_container.NFA()
        ffa3 = items3_container.FFA()
        wfa3 = items3_container.WFA()
        bfa3 = items3_container.BFA()

        nfa3_table, nfa3_rows, nfa3_cols = containers_to_table(nfa3)
        ffa3_table, ffa3_rows, ffa3_cols = containers_to_table(ffa3)
        wfa3_table, wfa3_rows, wfa3_cols = containers_to_table(wfa3)
        bfa3_table, bfa3_rows, bfa3_cols = containers_to_table(bfa3)
        
        algorithm_complexity_nfa3 = items3_container.algorithm_complexity_nfa
        algorithm_complexity_ffa3 = items3_container.algorithm_complexity_ffa
        algorithm_complexity_wfa3 = items3_container.algorithm_complexity_wfa
        algorithm_complexity_bfa3 = items3_container.algorithm_complexity_bfa
        
        nfa3s = items3_container.NFA(sort=True)
        ffa3s = items3_container.FFA(sort=True)
        wfa3s = items3_container.WFA(sort=True)
        bfa3s = items3_container.BFA(sort=True)
        
        nfa3s_table, nfa3s_rows, nfa3s_cols = containers_to_table(nfa3s)
        ffa3s_table, ffa3s_rows, ffa3s_cols = containers_to_table(ffa3s)
        wfa3s_table, wfa3s_rows, wfa3s_cols = containers_to_table(wfa3s)
        bfa3s_table, bfa3s_rows, bfa3s_cols = containers_to_table(bfa3s)
        
        algorithm_complexity_nfa3s = items3_container.algorithm_complexity_nfa
        algorithm_complexity_ffa3s = items3_container.algorithm_complexity_ffa
        algorithm_complexity_wfa3s = items3_container.algorithm_complexity_wfa
        algorithm_complexity_bfa3s = items3_container.algorithm_complexity_bfa
        
        context.update({
            'nfa3': nfa3_table, 'nfa3_rows': nfa3_rows, 'nfa3_cols': nfa3_cols,
            'ffa3': ffa3_table, 'ffa3_rows': ffa3_rows, 'ffa3_cols': ffa3_cols,
            'wfa3': wfa3_table, 'wfa3_rows': wfa3_rows, 'wfa3_cols': wfa3_cols,
            'bfa3': bfa3_table, 'bfa3_rows': bfa3_rows, 'bfa3_cols': bfa3_cols,
            
            'nfa3s': nfa3s_table, 'nfa3s_rows': nfa3s_rows, 'nfa3s_cols': nfa3s_cols,
            'ffa3s': ffa3s_table, 'ffa3s_rows': ffa3s_rows, 'ffa3s_cols': ffa3s_cols,
            'wfa3s': wfa3s_table, 'wfa3s_rows': wfa3s_rows, 'wfa3s_cols': wfa3s_cols,
            'bfa3s': bfa3s_table, 'bfa3s_rows': bfa3s_rows, 'bfa3s_cols': bfa3s_cols,
            
            'algorithm_complexity_nfa3': algorithm_complexity_nfa3,
            'algorithm_complexity_ffa3': algorithm_complexity_ffa3,
            'algorithm_complexity_wfa3': algorithm_complexity_wfa3,
            'algorithm_complexity_bfa3': algorithm_complexity_bfa3,

            'algorithm_complexity_nfa3s': algorithm_complexity_nfa3s,
            'algorithm_complexity_ffa3s': algorithm_complexity_ffa3s,
            'algorithm_complexity_wfa3s': algorithm_complexity_wfa3s,
            'algorithm_complexity_bfa3s': algorithm_complexity_bfa3s,
        })
        
        #! for items 1+2+3
        items123_container = Containers(capacity=capacity)
        items123_container.add_item(items1)
        items123_container.add_item(items2)
        items123_container.add_item(items3)
        
        nfa123 = items123_container.NFA()
        ffa123 = items123_container.FFA()
        wfa123 = items123_container.WFA()
        bfa123 = items123_container.BFA()
        
        nfa123_table, nfa123_rows, nfa123_cols = containers_to_table(nfa123)
        ffa123_table, ffa123_rows, ffa123_cols = containers_to_table(ffa123)
        wfa123_table, wfa123_rows, wfa123_cols = containers_to_table(wfa123)
        bfa123_table, bfa123_rows, bfa123_cols = containers_to_table(bfa123)
        
        algorithm_complexity_nfa123 = items123_container.algorithm_complexity_nfa
        algorithm_complexity_ffa123 = items123_container.algorithm_complexity_ffa
        algorithm_complexity_wfa123 = items123_container.algorithm_complexity_wfa
        algorithm_complexity_bfa123 = items123_container.algorithm_complexity_bfa
        
        nfa123s = items123_container.NFA(sort=True)
        ffa123s = items123_container.FFA(sort=True)
        wfa123s = items123_container.WFA(sort=True)
        bfa123s = items123_container.BFA(sort=True)
        
        nfa123s_table, nfa123s_rows, nfa123s_cols = containers_to_table(nfa123s)
        ffa123s_table, ffa123s_rows, ffa123s_cols = containers_to_table(ffa123s)
        wfa123s_table, wfa123s_rows, wfa123s_cols = containers_to_table(wfa123s)
        bfa123s_table, bfa123s_rows, bfa123s_cols = containers_to_table(bfa123s)
        
        algorithm_complexity_nfa123s = items123_container.algorithm_complexity_nfa
        algorithm_complexity_ffa123s = items123_container.algorithm_complexity_ffa
        algorithm_complexity_wfa123s = items123_container.algorithm_complexity_wfa
        algorithm_complexity_bfa123s = items123_container.algorithm_complexity_bfa
        
        analytical_min1 = math.ceil(sum(items1) / capacity)
        analytical_min2 = math.ceil(sum(items2) / capacity)
        analytical_min3 = math.ceil(sum(items3) / capacity)
        analytical_min123 = math.ceil(sum(items1 + items2 + items3) / capacity)

        context.update({
            'analytical_min1': analytical_min1,
            'analytical_min2': analytical_min2,
            'analytical_min3': analytical_min3,
            'analytical_min123': analytical_min123,
        })

        context.update({
            'nfa123': nfa123_table, 'nfa123_rows': nfa123_rows, 'nfa123_cols': nfa123_cols,
            'ffa123': ffa123_table, 'ffa123_rows': ffa123_rows, 'ffa123_cols': ffa123_cols,
            'wfa123': wfa123_table, 'wfa123_rows': wfa123_rows, 'wfa123_cols': wfa123_cols,
            'bfa123': bfa123_table, 'bfa123_rows': bfa123_rows, 'bfa123_cols': bfa123_cols,
            
            'nfa123s': nfa123s_table, 'nfa123s_rows': nfa123s_rows, 'nfa123s_cols': nfa123s_cols,
            'ffa123s': ffa123s_table, 'ffa123s_rows': ffa123s_rows, 'ffa123s_cols': ffa123s_cols,
            'wfa123s': wfa123s_table, 'wfa123s_rows': wfa123s_rows, 'wfa123s_cols': wfa123s_cols,
            'bfa123s': bfa123s_table, 'bfa123s_rows': bfa123s_rows, 'bfa123s_cols': bfa123s_cols,
            
            'algorithm_complexity_nfa123': algorithm_complexity_nfa123,
            'algorithm_complexity_ffa123': algorithm_complexity_ffa123,
            'algorithm_complexity_wfa123': algorithm_complexity_wfa123,
            'algorithm_complexity_bfa123': algorithm_complexity_bfa123,
            
            'algorithm_complexity_nfa123s': algorithm_complexity_nfa123s,
            'algorithm_complexity_ffa123s': algorithm_complexity_ffa123s,
            'algorithm_complexity_wfa123s': algorithm_complexity_wfa123s,
            'algorithm_complexity_bfa123s': algorithm_complexity_bfa123s,
        })
        
        return render(request, 'core/index.html', context)


index = Index.as_view()

def start_page(request):
    variant_range = [
        {
            'slug': f"variant-{i}", 
            'name': f"{i}"
        }  
        for i in range(1, 31)
    ]
    variant_test = [
        {
            'slug': f"variant-test", 
            'name': f"Тестовий з методички"
        },
        {
            'slug': f"variant-enter", 
            'name': f"Ввести власнору варіант"
        }  
    ]
    return render(request, 'core/start_page.html', {'variant_range': variant_range, 'variant_test': variant_test})