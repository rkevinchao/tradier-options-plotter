style = dict(style_name    = 'classic',
             base_mpl_style= 'fast', 
             marketcolors  = {'candle'  : {'up':'w', 'down':'k'},
                              'edge'    : {'up':'k', 'down':'k'},
                              'wick'    : {'up':'k', 'down':'k'},
                              'ohlc'    : {'up':'k', 'down':'k'},
                              'volume'  : {'up':'#181818', 'down':'#181818'},
                              'vcedge'  : {'up':'#181818', 'down':'#181818'},
                              'vcdopcod': False, # Volume Color is Per Price Change On Day
                              'alpha'   : 0.9,
                             },
             mavcolors     = ['#1a1a1a','#262626','#333333','#404040'],
             y_on_right    = True,
             gridcolor     = '#cccccc',
             gridstyle     = '--',
             facecolor     = 'w',
             rc            = [ ('axes.edgecolor'  , 'black'   ),
                               ('axes.linewidth'  ,  1.5      ),
                               ('axes.labelsize'  , 'large'   ),
                               ('axes.labelweight', 'semibold'),
                               ('lines.linewidth' ,  2.0      ),
                              #('patch.force_edgecolor', True ),
                               ('font.weight'     , 'medium'  ),
                               ('font.size'       ,  12.0     ),
                             ],
             base_mpf_style= 'classic'
            )
